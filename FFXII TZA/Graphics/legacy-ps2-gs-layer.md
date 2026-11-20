[Home](../../README.md) / [Graphics](README.md) / Legacy PS2 GS layer

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Legacy PS2 GS layer: the GS memory model, the map texture slot rebuild and the VU register leftovers | system | Graphics | Render pipeline | What the remaster keeps of the PlayStation 2 Graphics Synthesizer model outside the VIF1 / VU1 emulation: the 512 x 448 surface seed and its three reserved surfaces, the GS page geometry of 0x003A1E50, the 4 MiB local-memory budget, the rebuild that gives the bound map's multiply used textures compact slots when the weather slot changes or a map is bound, the per-pass reset of those slots, the GS image-transfer registers, and the VU register words that recompiled microprograms use for Q and vf00. | 0x0036D280, 0x0036D2F0, 0x022D8EAC, 0x022D8EB4, 0x022D8EA8, 0x003A1E50, 0x00466190, 0x00466220, 0x00467AA0, 0x00467AD0, 0x00467B00, 0x00467B10, 0x002F7380, 0x0026E290, 0x0026E8D0, 0x0209A670, 0x0209A6E8, 0x0209A708, 0x002F4520, 0x00244200, 0x004B9870, 0x01E02830, 0x02064B00 |

## What the player sees

Nothing directly. The PC renderer draws at the display resolution, but a layer of the
PlayStation 2 code still runs underneath it with the console's numbers: a 512 × 448 frame, a
4 MiB Graphics Synthesizer local memory of 8 KiB pages, and a texture budget computed against
it. When a field's weather slot changes or a map is bound, the game recounts which of the map's textures are used
more than once and gives as many of them as fit in that budget a compact slot.

The VIF1 packet decoder, the recompiled VU1 microprograms and the GS replay are on
[PS2 VIF1 and VU1 emulation](../Engine-Core/ps2-vif1-vu1-emulation.md); this page covers
the rest of the GS model.

## How it works

### The surfaces

`0x0036D280` seeds the GS globals: width `0x022D8EAC` = `0x200`, `0x022D8EB0` = `0x200`, height
`0x022D8EB4` = `0x1C0`, frame index `0x022D8EA8` = 0, the clear colour `0x022D8ED8` = 0 with its switch
`0x022D8EDC` = 1, and `0x022D8EE0` = 1. Those stores at `0x0036D286`, `0x0036D2A3`, `0x0036D2AD` and
`0x0036D290` are the only stores that name the three dimension words and the frame index. One 8-byte
store also zeroes `0x022D8EBC` and `0x022D8EC0`¹. It then calls `0x0016D6A0`, a bare `ret`, twice
and tail-jumps to `0x0036D2F0`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0036D296` |
| ² | `0x0036D2E6` |

</details>

`0x0036D2F0` then computes the pages per surface, `(width × height) >> 11` = 112 GS pages of 2,048
words, into `0x022D8EB8`¹, fills the two 0x28-byte display records at `0x022D8E50` and
`0x022D8E78`, and points `0x022D8EA0` at the first. The GS register batch `0x0036D400` places the colour
surface at page `index × 112` with PSM 0 and the Z surface at page 224 with bit `0x1000000` set
([graphics thread handshake](graphics-thread-handshake.md)). With the index at 0 the frame uses
surfaces 0 and 2 of the three the budget reserves.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0036D393` |

</details>

### GS page geometry

`0x003A1E50(width, height, psm)` returns a texture's footprint in 32-bit words, rounded up to whole
GS pages: `((height + ha - 1) & ~(ha - 1)) x ((width + wa - 1) & ~(wa - 1)) / d`, with the width align `wa`,
height align `ha` and divisor `d` of the table below¹.
It indexes the 43-byte table `0x003A1EF0` with `psm − 2`; an index above `0x2A`, which
includes PSM 0 and 1 through the unsigned compare at `0x003A1E68`, takes the default class. The
class picks an arm from `0x003A1EE0`:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003A1EBA`-`0x003A1ED8` |

</details>

| Class | PSMs | Width align | Height align | Divisor | Smallest footprint |
|---|---|---:|---:|---:|---:|
| default (`0x003A1EBA`) | all others, including `0x00`, `0x01` | 64 | 32 | 1 | 2,048 words |
| 0 (`0x003A1E96`) | `0x02`, `0x0A` | 64 | 64 | 2 | 2,048 words |
| 1 (`0x003A1E9E`) | `0x13`, `0x1B` | 128 | 64 | 4 | 2,048 words |
| 2 (`0x003A1EAD`) | `0x14`, `0x24`, `0x2C` | 128 | 128 | 8 | 2,048 words |

These are the GS page sizes of the 32-, 16-, 8- and 4-bit pixel formats. `0x00466190(bank, index)`
sums `0x003A1E50` over a texture record's mip levels, halving width and height each level, with the
level count at `+0x05` capped at 7¹. `0x00466220(record)` returns 1 exactly for
PSMs `0x14`, `0x24` and `0x2C`: `(psm − 0x14) & 0xE7` must be 0 and `psm` must not be `0x1C`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x004661C5`-`0x004661CC` |

</details>

### The budget

`0x00467AD0` stores `0x4000` at `0x02CA5FF0` and the reservation `(width × height × 3) >> 6` at
`0x02CA5FF4`: 10,752 blocks of 64 words. `0x00467AA0` returns the budget

```python
budget = (0x1007FF - 3 * width * height - [0x02CA6008] - [0x02CA6004]) & 0xFFFFF800
```

that is, the 4 MiB memory (`0x100000` words) less three 512 × 448 surfaces at 4 bytes per pixel,
less the two totals the rebuild publishes, rounded up to a whole page. With both totals at 0 it is
360,448 words: 1.375 MiB, 176 pages. The surface size is fixed, so the budget does not depend on
the display resolution.

Once its refusals are passed¹, each pass of the slot handler `0x002F4520` calls `0x00467A70`², which sets the cursor `0x02CA5FF8` back to the reservation `0x02CA5FF4` and zeroes `0x02CA5FFC` and
`0x02CA6000`; `0x00467A90` returns the cursor.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002F458B`-`0x002F45B9` |
| ² | `0x002F45D9` |

</details>

`0x002D7FC0`, run by the frame set-up `0x0024D540`, clears the two `0x1800`-byte blocks at `0x02F8DA00` and
`0x02F8C200`, keeps the width `0x022D8EAC` at `0x02F8F214` and places five block addresses after the surfaces,
moving them up by `(width - 0x200) x 0x540 / 64` for a width above `0x200` (0 at the shipped 512):

| Address | Value |
|---|---|
| `0x02F8F200` | `0x3B00` |
| `0x02F8F204` | `0x2A00` + d |
| `0x02F8F208` | `0x3C00` + d |
| `0x02F8F20C` | `0x3B00` + d |
| `0x02F8F210` | `0x3C00` + d |

### The surfaces as textures

`0x0039D200`, run by the same frame set-up¹, rewrites six 16-byte entries at `0x02AEECF0`, each
a pair of values in the layout of the GS registers TEX0 and CLAMP, for draws that sample the surfaces:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0024D560` |

</details>

| Entries | TEX0 value | CLAMP value | Base page (TEX0 bits `0x3FFF`) |
|---|---|---|---|
| `0x02AEECF0`, `0x02AEED00` | `0x664100000` with `width / 64` in the bits under mask `0xFC000`: PSM 1, 512 × 512, TCC 1 | `10` (region clamp in u and v), maximum u = width − 1, v = height − 1 | `width × height / 64` in one of the two, 0 in the other |
| `0x02AEED10` to `0x02AEED40` | `0x620110000`: PSM 1, 256 × 256, TCC 1 | `10` with half the width and height | `0x3C00`, `0x3700`, `0x3300`, `0x3FFF` |

The full-size base goes into the first entry when bits `0x1FF` of the FRAME_1 value `0x022D8EC8` are 0, and
into the second otherwise. Readers of the entries include `0x0024B7B0`, `0x0036F550`, `0x0036F9F0`,
`0x00374280`, `0x003745C0`, `0x00431830` and `0x004FD4B0`.

### GS screen coordinates

The map draw still builds the screen transform of the PS2 drawing area. `0x00467940(view)` writes into
the first 64 bytes of a view block a matrix that maps x to `x × w / 2 + 2048`, y to `−y × h / 2 +
2048` and z to `−z × (far − near) / 2 + (far + near) / 2`. The width `w` and height `h` are the
integers at `+0x44` and `+0x48` of the same block and the two depths are at `+0x4C` and `+0x50`;
2048 is the centre of the GS drawing coordinates.

`0x00276430(…, widget, x, y, u, v, rect, scale)`, run by `0x00272590`, sets the same kind of transform for a 2D
widget draw: an identity matrix at `0x0209AB90` scaled by `scale`, the offset `2048 - screen / 2 + x` and
`+ y` from the screen size `0x01E0C1D8`, `0x01E0C1DC`, the widget's position `/ 4096`, its colour bytes `/ 128`
and the four-word rectangle; it first writes the widget's colour scaled by its brightness `+0x5A` and alpha
`+0x58` into `+0x94`: `rgb = (byte +0x90..+0x92 x s16 +0x5A) >> 7` and `a = (byte +0x93 x s16 +0x58) >> 7`¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0027643F`-`0x0027649F` |

</details>

The draw-list build `0x002F5550` calls it¹ on a stack copy of the view block at
`0x02AED500` whose depths it has replaced by `0x003B40B0` results, and copies the matrix to `+0x80` of
each `0xE0`-byte record of the map's tag-24 array (`[+0x1D0]`, count `+0x220`).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002F5AB0` |

</details>

The slot handler `0x002F4520` calls `0x00467B60`¹, which stores
`int(−16 × log2|20 − c|)` in the high dword of `0x02EBB6C8`, with `c` the float at `0x02AED570`, the
working camera's `+0x10`. `0x00467BB0` zeroes the same qword at start-up; these two stores are the only
instructions that name it.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002F4670` |

</details>

### When the rebuild runs

The bound map is the object at `0x0209A670` ([MPK map pack](../World-Areas-And-Travel/mpk-map-pack.md)).
`0x0026E8D0(slot)`, the weather rebind ([weather](../World-Areas-And-Travel/weather.md)), stores the slot
at `0x0209A6E8` and sets the dirty word `0x0209A708`¹; `0x0026E960` sets it too when a map
is bound². These are its only two non-zero stores; the reset `0x0026E1D0` clears it. The stores of 1 at
`0x0026E221` and `0x0026E9A6` go to the neighbouring word `0x0209A6FC`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0026E8E7` |
| ² | `0x0026E9B0` |

</details>

The draw's pass bit `0x1` block calls `0x0036F430` and `0x0036F450`, which call `0x0026E290` with 0 and 1.
While a map is bound and its `+0x120` is non-zero, `0x0026E290` runs `0x002F7380(map, [0x0209A668])` when
the dirty word is set and then clears it¹, and then calls the map's
`+0x130` handler with the pass when the handler is set²; with no map or a `+0x120`
of 0 it returns at once³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0026E2C4`, `0x0026E2C9` |
| ² | `0x0026E2D3`-`0x0026E2E4` |
| ³ | `0x0026E2A6`, `0x0026E2AF` |

</details>

That handler is `0x002F4520`, installed by the map set-up
`0x002F6AB0`¹. It returns at once when the map's data `+0x158` is 0, its `+0x234` is 0 or the pass's draw
list is empty²; otherwise, after `0x00467A70` and `0x00467A90`, it sets `+0x00` of every slot
record to 0 and `+0x20` to `0xFF`³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002F6B43` |
| ² | `0x002F458B`-`0x002F45B9` |
| ³ | `0x002F45F0`-`0x002F4617` |

</details>

The map's file reaches the set-up through an eight-slot table at `0x02EBB820` (`0x38` bytes a slot:
`+0x00` the data, `+0x08` a count, `+0x10` a word set to 2, `+0x14` a name). The binders `0x0026E760`
and `0x0026E7D0`, both from `0x00378120`, register the data with `0x003EC9A0`, which takes the next free
slot from a round-robin cursor: `slot = [0x02EBB9E0]`, then `[0x02EBB9E0] = ([0x02EBB9E0] + 1) % 8`, repeated while
`slot` holds data, at most eight times; a free slot adds 1 to `0x02EBB9E4`¹. It writes a
fixed placeholder name and returns the slot number.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003EC9A0`-`0x003ECA66` |

</details>

The set-up `0x002F6AB0` stores the number at map `+0x168` and reads the
slot back with `0x003EC970(n)` (null past 7 or for an empty slot), keeping the data at `+0x158` and the
name at `+0x160`. The map teardown `0x002F5450` releases it with `0x003ECA70(n)`, which frees the data
when the count is positive¹ and clears the slot.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003EC8A0` |

</details>

`0x00862910` truncates a float vector to four integers, and `0x00862930` does the same after scaling by
16, the GS coordinate form. The model instance's draw setup `0x004FD4B0` converts the instance's
`+0xD0` with the first and writes the fourth integer into the bits under mask `0xFF00000000000000` of the GS FOG register
(`0x0A`); the point projector `0x00272180` and the map screen code `0x003C29A0` use the second.

### The texture record bank

YM00 tags 14 and 26 build the bank at the map's `[+0x150]` with `0x00467D20(bank, chunk)` ([map
pack](../World-Areas-And-Travel/mpk-map-pack.md)). The chunk starts with a count dword and that many index dwords from
`+0x04`; the low 24 bits of each, times 16, place a record in the chunk, whose TIM2 image is at `+0x30`. The bank
keeps the chunk at `+0x18`¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00467D36` |

</details>

A first pass adds up the picture counts, the word at TIM2 `+0x06`¹. The old record array
`+0x08` is freed², the total goes to the bank's `+0x00`³, and a zeroed array of
`total * 0x60` bytes from arena 6 takes its place⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00467D54`-`0x00467DB4` |
| ² | `0x003EC8A0`, `0x00467DC6` |
| ³ | `0x00467DD0` |
| ⁴ | `0x00467DD2`-`0x00467DF9` |

</details>

A second pass fills one record per picture, the records in index order and each record's pictures in turn, numbering
on from one record to the next¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00467E30`-`0x00468037` |

</details>

`0x00536080(tim2, j)` finds picture `j`: it answers null for `j` at or past the count, and otherwise starts after the
TIM2 header (`+0x10`, or `+0x80` when byte `+0x05` is not 0) and steps over `j` pictures by each one's size dword
`+0x00`¹. The fields each record gets are in [the texture record layout](#layouts). Its
pointers are stored as `0x0020E620(p)`, the 32-bit `p` less the dword `0x01F83530`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00536080`-`0x005360BB` |
| ² | `0x0020E620`-`0x0020E628` |

</details>

### The slot rebuild

`0x002F7380(map)` works on the map's texture records (a bank at `[+0x150]`: count at `+0x00`,
0x60-byte records from `[+0x08]`) and its instance records (`[+0x178]`, 0x30 bytes, count `+0x174`):

| Step | What happens | Where in the code |
|---|---|---|
| 1 | free the old slot table at `+0x218` and copy the bank's count to `+0x224`; | `0x003EC8A0` |
| 2 | for every texture record: track the largest mip-chain footprint, add 1 for a 4-bit record or 4 for any other to a second total, and set the word `+0x0E` to 0; | `0x00466190`, `0x002F7436`-`0x002F743B`<br>`0x002F744A`-`0x002F7455`<br>`0x002F7445` |
| 3 | publish the largest footprint to `0x02CA6004` and the total to `0x02CA6008`, then take the budget from `0x00467AA0`; | `0x00467B10`<br>`0x00467B00` |
| 4 | for every instance record whose flag word `+0x0C` has bit `23 + slot` set and whose texture index `+0x04` is at most `0x3FFF`, unless it repeats the texture index and byte `+0x1D` of the last record counted: increment `+0x0E` of that texture record and of each record after it up to the first whose `+0x0C` word is 0 or the bank count `+0x224`; | `0x002F738E`-`0x002F7397`, `0x002F74C9`<br>`0x002F74D4`-`0x002F74E3`<br>`0x002F7500`<br>`0x002F7504`-`0x002F753D` |
| 5 | walk the texture records in bank order: a record counted more than once is admitted when the running total plus its footprint stays below the budget, and gets the next slot number in `+0x0E`; every other record gets `0xFFFF`. A record that does not fit is skipped and the walk goes on, so a smaller record later in the bank can still be admitted; | `0x002F75A2`<br>`0x002F75B0` |
| 6 | with any admitted, store the count at `+0x228`, allocate `count × 40` bytes (`0x003EC8D0(6, …)`) at `+0x218`, and zero `+0x00`, `+0x08`, `+0x10`, `+0x18` and the byte `+0x20` of each record. | `0x002F760B`-`0x002F761F` |

The texture index and byte `+0x1D` that step 4 compares with start at -1¹ and change only when a record is counted². A texture record past
one whose `+0x0C` word is 0 is not counted by that run.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002F73DE`-`0x002F740A`, `0x002F7465`-`0x002F7474` |
| ² | `0x002F753F`-`0x002F7542` |

</details>

Only the records after the first are tested against `+0x224`: step 4's first increment goes to the index the instance
names, up to `0x3FFF`, so an index at or past the bank count writes past the array¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002F74E5`-`0x002F7500` |

</details>

`0x003EC8D0` reports a failed allocation by passing `"out of memory!\n"` to `0x00862690`, which hands
it to `0x008620B0`, a body that returns at once; nothing is printed.

### GS image transfers

`0x00244200`, called from `0x002D2DB0`, writes GS register records for image transfers: BITBLTBUF
`0x50`, TRXPOS `0x51`, TRXREG `0x52` and TRXDIR `0x53`¹, then TRXPOS, TRXREG
and TRXDIR again². It reads the frame index and the height to place the
transfer. The GS replay honours none of these four registers.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002442D2`-`0x00244332` |
| ² | `0x00244355`-`0x0024439C` |

</details>

`0x00244200(widget)` first copies the frame into id `0x333C` with `0x0039D0C0(0, 0x333C, 0x200, 0x1C0, 0, 1, 0)`¹, then opens one A+D GIF tag of seven registers with the end-of-packet bit² and closes it with `0x00248E10`³. The values:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0024427B` |
| ² | `0x00248EB0`, `0x002442A2`-`0x002442B9` |
| ³ | `0x002443AA` |

</details>

- BITBLTBUF: source base `([0x022D8EA8] x [0x022D8EB4] x [0x022D8EAC]) >> 6`, source and destination width
  `[0x022D8EAC] >> 6` and destination base `0x333C`¹;
- both TRXREG: 16 rows of `[0x022D8EAC]` pixels, and both TRXDIR 2²;
- the first TRXPOS: source row `max(y, 0)` to row 0, with `y` the widget's `s16` `+0x52`³;
- the second TRXPOS: source row `min(y + h - 16, [0x022D8EB4] - 16)`, with `h` the `s16` `+0x56`, to row 16
 ⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0024422E`-`0x00244278` |
| ² | `0x0024430F`, `0x0024432B`, `0x00244375`, `0x00244393` |
| ³ | `0x0024428B`-`0x002442EF` |
| ⁴ | `0x0024421E`-`0x00244244`, `0x00244280`-`0x00244295`, `0x00244343`-`0x00244352` |

</details>

`0x002443D0(widget, node)`, also called from `0x002D2DB0`¹, sets node `+0x38` bit `0x100`, clears bits `0x3E00`,
and stores at node `+0x30` a TEX0 word: the constant `0x40010333C` (base `0x333C`, format 1, TCC set) with the
buffer width `0x022D8EAC` / 64, TW the highest set bit of 2 x width - 1 (9 for the shipped `0x200`) and TH 5, from
`0x3F`. It then writes TEXA (`0x3B`) = `0x80` under one A+D GIF tag².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002D2F30` |
| ² | `0x00248EB0`, `0x00248E10` |

</details>

`0x003A22A0(packet, base, format, width, height, data)` builds a whole upload into a packet. It opens an
A+D GIF tag¹ and writes BITBLTBUF with the destination base in the bits under mask `0x3FFF00000000`, the buffer
width from `0x003A1FE0` in the bits under mask `0x3F000000000000` and the format in the bits under mask `0x3F00000000000000`, then TRXPOS 0, TRXREG
`width, height` and TRXDIR 0, and closes the tag². The image follows through
`0x003A21A0`, and a second A+D tag writes TEXFLUSH (`0x3F`).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003A2090` |
| ² | `0x0024B150` |

</details>

The data size is `0x003A1F20(width, height, format) / 4`¹.
`0x003A1F20` takes `n = width x height` and returns `n x 3 / 2` for
formats `1` and `0x31`, `n / 2` for `2`, `0x0A`, `0x32` and `0x3A`, `n / 4` for `0x13` and `0x1B`, `n / 8` for
`0x14`, `0x24` and `0x2C`, and `n` otherwise².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003A22E0`-`0x003A22EF` |
| ² | `0x003A1F20`-`0x003A1F8C` |

</details>

- `0x003A1FE0(width, format)` is the buffer width in 64-pixel units: the width rounded up to a
  multiple of 64, or to a multiple of 128 for the formats `0x13`, `0x14`, `0x1B`, `0x24` and `0x2C`
  (the 8-bit and 4-bit indexed ones), divided by 64.
- `0x003A21A0(packet, qwords, data)` splits the image into pieces of at most `0x4000` quadwords. Each
  piece is a DMA `cnt` tag with a VIF `DIRECTHL` of one quadword carrying an IMAGE-mode GIF tag for
  the piece, then a DMA `ref` tag with a second `DIRECTHL` that points at the piece's place in the
  data. `0x0024AF50` and `0x003EFDF0` call it directly.

`0x0039D0C0(mode, id, width, height, target, a, b)` copies the rendered frame into the target of a GS
texture id. With no target given it takes the id's own¹, or a new one from `0x00182B40`
when the id lacks one. It closes an open scene around the copy (`0x001FBE30`, `0x001FBE50`, then
`0x001FBD80`), copies through `0x00182A60`, whose source the first argument picks², with a
mode of 0 to 3 chosen from `a` and `b`³, and records a changed target for the id⁴. `0x00244200` calls it for id `0x333C` at
512 × 448; `0x003749F0`, `0x00376220` and `0x003A2BD0` are the others.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002D7FA0` |
| ² | `0x00186910` |
| ³ | `0x00376320` |
| ⁴ | `0x002D7D90` |

</details>

A texture word in the GS TEX0 layout comes from `0x002D8050(word, width, height, format)`. It keeps the
base in bits `0x3FFF`, which the caller sets, and writes the other fields, with e(n) the exponent below:

- the buffer width in 64-pixel units, in bits `0xFC000`: the field takes `(width / 64) & 0x3F`
 ¹, a non-zero `width % 64` adds 1 that wraps in 6 bits², and a
  field of 1 becomes 2³; with `w = width / 64 + (width % 64 != 0)` that is
  `f = w & 0x3F`, then `f == 1 ? 2 : f`, so a width of 4,097 to 4,160 pixels stores 2;
- the format in bits `0x3F00000`, `(format & 0x3F) << 20`⁴;
- the power-of-two exponents of the width and height in the bits under mask `0x3FC000000`, and bit `0x400000000`:
  `(e(width) & 0xF) << 26` and `((e(height) & 0xF) | 0x10) << 30`⁵;
- bits `0x800000000` and `0x1000000000` are cleared, by the mask `0xFFFFFFE43FFFFFFF`⁶.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002D805F`-`0x002D8088` |
| ² | `0x002D808E`-`0x002D80AC` |
| ³ | `0x002D80AF`-`0x002D80DC` |
| ⁴ | `0x002D80DF`-`0x002D80F2` |
| ⁵ | `0x002D80F5`-`0x002D8134` |
| ⁶ | `0x002D8120`, `0x002D812E` |

</details>

The exponent is `0x002D8150(n)`, the smallest e with 2^e ≥ n for n up to 1024, and 11 for a larger n¹. The effect-texture placer `0x002D83B0` builds
its words this way. The way back is `0x002D7F20(e)`: 2^e for e up to 10, 0 above. The screen-effect
upload `0x00375B90` (kind 4) reads the width and height out of its word `+0x30` with it and passes
them, with the base and the format, to `0x003A22A0`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002D81A0`-`0x002D81AE` |

</details>

A second exponent helper, `0x003666E0(n)`, returns log2 n for a power of two `n`; its two callers are `0x003649A0` and
`0x00474710`. `0x00474710` builds a GS sprite packet of register and value pairs, registers `0x3F`, `0x4C`, `0x06`
(TEX0) and `0x42` (ALPHA, value `0x44`)¹, with the colour `0x80808080`², and
divides its two texture coordinates by `1 << 0x003666E0` of each texture dimension³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00474F95`-`0x00474FF5` |
| ² | `0x0047502A` |
| ³ | `0x00475044`, `0x00475066` |

</details>

### The VIF packet writer

The map screens, the world map and the battle target lines still build VIF1 packets for VU1 in the GS
command buffers ([render command list](render-command-list.md)). They use a writer of pointers on the
caller's stack and a family of helpers around `0x00271450`:

| Helper | Does |
|---|---|
| `0x00271450(w)` | starts at the current buffer: `+0x00` the buffer record, `+0x08` and `+0x10` its write cursor |
| `0x00271360(w, other)` | continues after another writer: same buffer, start at its cursor, cursor 16 bytes on |
| `0x002714A0`, `0x002714C0`, `0x00271480` | reserve the record at the cursor as the chunk header `+0x18`, the GIF tag slot `+0x28` or the DIRECT header `+0x30` |
| `0x00272390(w, records, n)` | copies `n` 16-byte records to the cursor and advances it; `0x00271290` copies without a writer |
| `0x00271080(w)` | closes a chunk: VIF FLUSH (`0x11000000`) and `0x10000000` in the header's upper dwords |
| `0x002710C0(w, eop)` | writes the GIF tag: A+D (`0xE`), one register, the record count as NLOOP and `eop` in bit `0x8000` |
| `0x00271100(w)` | writes an UNPACK header (`0x6C008000` with the count in the bits from `0x10000` up) after three `0x10000000` |
| `0x00271050(w)` | writes a DIRECT header: `0x13000000` (FLUSHA), `0x10000000`, `0x50000000` with the count |
| `0x002712E0(w, src, ad)` | closes a DIRECT chunk of `src`, with an A+D end record `{0x8000, 0xE}` when `ad` is 1 |
| `0x00270FF0(w)`, `0x00271010(w, n)` | end the packet: when anything was written, advance the buffer's cursor and flip it (`0x003A1DB0`) |

Each closer computes its chunk's record count and passes the header to `0x0016D6A0`, a bare `ret`, so the
DMA tag in the first qword of every chunk header is never written.

The content helpers write fixed packets:

- `0x00271760(w, block, matrix, extra)` builds a 15-record chunk: an UNPACK header for 13 records¹, the 13
  records of the block's constant area, and FLUSHA, MSCAL².
- `0x00276190` fills ten of the chunk's 13 constant records: records 0 to 3 with the matrix, 4 to 7 with the matrix
  `0x02AEDDB0` ([scripted camera](scripted-camera.md)), record 8 with four times 2047.5 and record 12 with four times
  1.0, that last record replaced by `extra` when given. Records 9 to 11 keep what the block holds.
- `0x00271720(w)` writes VIF BASE 0 and OFFSET `0x200`³ into the record at
  the cursor. `0x002715A0(w, picture, row, half)` writes a picture bind there: A+D with CLAMP_1 = 5 and
  TEX0_1 from the picture's `+0x30`, the palette offset `(half + row × 2) × 2` in the bits from `0x2000000000` up.
- Both, and `0x00271870(w, data, bytes)`, store back the cursor value they read and nothing between
  moves it, so the next write lands on the same records. `0x00271870` passes `bytes / 16` and `data`
  to `0x0016D6A0`, so it copies nothing.
- Three helpers write records at a plain pointer and return the pointer past them; the HUD's target rings
  and `+0x10F30` marks use them⁴.
- `0x00271530(p, eop, flat)` writes a four-register A+D packet: TEST_1 `0x53001`, ALPHA_1 `0x44`,
  PRMODECONT 1 and PRIM `0x5C` (a textured, blended, shaded triangle strip), or `0x54` without shading
  when `flat` is non-zero.
- `0x00271650(p, picture, row, half, eop)` writes a two-register picture bind, CLAMP_1 = 5 and TEX0_1 from
  the picture's `+0x30` with the palette offset `(half + row x 2) x 2` in the bits from `0x2000000000` up.
- `0x002716C0(p, end)` writes FLUSHA, NOP and a DIRECT header counting the records from `p + 0x10` to `end`.
- `0x002724A0(w)` ends a VU1 draw: the record at `[w + 0x38]` gets a GIF tag with end-of-packet, NLOOP
  `[w + 0x40]` and the registers ST, RGBAQ, XYZF2 (`0x412`); it completes the UNPACK header at
  `[w + 0x20]`, appends FLUSHA and MSCNT⁵, closes the chunk and ends the packet.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x6C0D8000` |
| ² | `0x13000000`, `0x14000000` |
| ³ | `0x03000000`, `0x02000200` |
| ⁴ | `0x0028C620`, `0x003F7CC0` |
| ⁵ | `0x17000000` |

</details>

- `0x00428980`, the last step of the character-record pass `0x004264A0` (from `0x00332440` and
  `0x00332510`), writes one DIRECT chunk into the current GS command buffer¹: an A+D GIF tag
  with end-of-packet², ZBUF_1 `0x4E` and ZBUF_2 `0x4F` from `0x022D8ED0`, FBA_1 `0x4A` = 0,
  TEST_1 `0x47` = `0x50000` (depth test, greater or equal) and ALPHA_1 `0x42` = `0x44`.
- `0x44` is the blend `(Cs − Cd) × As + Cd`. `0x003A2020` fills the tag's loop count, `0x00428980` gives
  the chunk header FLUSH and DIRECT with the record count, and `0x00504490` flips the buffer
 ³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x005044B0` |
| ² | `0x003A2090` |
| ³ | `0x003A1DB0` |

</details>

### VU register words outside VU memory

Recompiled VU1 microprograms keep VU registers in fixed globals next to the emulated VU memory
`0x02064E30`:

- `0x02064B00` is a scratch cell shared by many recompiled programs from `0047xxxx` to `0054xxxx`, and
  by a few effect routines¹.
- One of its writers is the division helper `0x004B9870`, which stores `a / b`, or
  `0x7F7FFFFF` (`0x00900360`, the largest float) when `b` is 0. The programs `0x004B1190` and `0x004C8320`
  load its address six times each and pass it to `0x004B9870` four times²: for those two programs it plays the VU's Q register.
- `0x01E02830` holds `(0, 0, 0, 1.0)`, the fixed contents of the VU's register vf00. `0x004B1190` loads
  its address 17 times as the second operand of its lane helpers, which include `0x004B9D80`,
  `0x004B9E60` and `0x004B9A10`. `0x0022CC20` writes those four words again; 63 functions call it.
- `0x004ADD10`, another installed program, reads VU memory cells directly through `0x02064E30`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002F05F8` |
| ² | `0x004B7C31`, `0x004B7CE4`, `0x004B895F`, `0x004B8A12` |

</details>

- Two shared subroutines of the recompiled programs work on the register cell `0x02064CB0`.
  `0x005375F0` (12 callers, `0x004758E0` among them) reduces its x lane by whole turns of 2π, using
  `1 / 2π` (0.15915494) and π. `0x005376D0` (13 callers) writes the sine and cosine of that lane to
  `0x02064CC0` and `0x02064CC4`.
- `0x005376D0` first folds the angle into `[−π/2, π/2]` and then sums the odd powers up to the ninth
  with the coefficients −0.16666657, 0.0083330255, −0.00019807414 and 2.601887e-06. Its
  comparisons go through `0x005379D0(flags, vector, value)`, which builds a VU MAC flag word: bits `0x80`
  to `0x10` for the lanes x to w below the value, bits `0x8` to `0x1` for the lanes equal to it.

## Layouts

<details>
<summary>Show the memory layouts</summary>

Texture record (map `+0x150` bank, from [`+0x08`]), `0x60` bytes, one per TIM2 picture¹:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00467D20` |

</details>

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | psm | GS pixel format: byte `0x00D12520` + 4 * (picture `+0x13` - 1)      `0x00467E9C`-`0x00467EAC` |
| `+0x01` | `u8` | 0 | written when the picture has a palette (byte `+0x12` not 0)    `0x00467FD0` |
| `+0x02` | `u8` | buffer width | `0x003A1FE0`(width, psm): the width rounded up to 128 for psm `0x13`, `0x14`, `0x1B`, `0x24` or `0x2C` and to 64 for the others, / 64  `0x00467EAE`-`0x00467EB3` |
| `+0x03` | `u8` | log2 of the width when it is a power of two: the top set bit of 2w-1 less | `0x00467EBB`-`0x00467F07` the highest clear bit below it, or 0; `+0x04` the same from the height        `0x00467F0B`-`0x00467F53` |
| `+0x05` | `u8` | levels | picture `+0x11`; capped at 7 by `0x00466190`                       `0x00467F69`-`0x00467F6E` |
| `+0x06` | `u16` | width | picture `+0x14`; halved per level                              `0x00467E8A`-`0x00467E8F` |
| `+0x08` | `u16` | height | picture `+0x16`; halved per level                              `0x00467E94`-`0x00467E98` |
| `+0x0A` | `u16` | colours | picture `+0x0E`, with a palette                                `0x00467FD4`-`0x00467FD9` |
| `+0x0C` | `u16` | continues | the picture's index in its TIM2; non-zero: counted with the record before it                                             `0x00467F7B` |
| `+0x0E` | `i16` | count, then slot | 0 when built; reference count during step 4; slot or `0xFFFF` after step 5 |
| `+0x10` | `u32` | 0x0020E620(0) | `0x00467F87` |
| `+0x14` | `u32` | image | `0x0020E620`(picture + word `+0x0C`)                               `0x00467F57`-`0x00467F64` |
| `+0x18` | `u32` | palette | `0x0020E620`(picture + dword `+0x08` + word `+0x0C`) with a palette, else `0x0020E620`(0)                                             `0x00467F78`, `0x00467FB9`-`0x00467FCD` |
| `+0x1C` | `u32` | 0x0020E620(picture) | `0x00467F84`-`0x00467F8F` |
| `+0x20` | `u32[16]` | 0x0020E620(0); tag 12 then stores 0x0020E620 of a slot of the array | `0x00467F92`-`0x00467FB1` [`0x02CA6018`], registered by `0x003CCB60`, at 4 * its chunk entry's `+0x08`    `0x004682B4`-`0x004682EB` |

Instance record (map `+0x178`, tag 30 of the map pack), `0x30` bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x02` | `i16` | placement row | read by `0x003A6FC0` |
| `+0x04` | `u16` |  | texture record index |
| `+0x0C` | `u32` | flags | bit `0x800000` + slot: present for that weather slot |
| `+0x1D` | `u8` | sub-index | a repeat of the previous index and sub-index is not counted again |

Slot record (map `+0x218`, count `+0x228`), `0x28` bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u64` |  | cleared at allocation and by `0x002F4520` on every pass it does not refuse |
| `+0x08` | `u64` |  | cleared at allocation |
| `+0x10` | `u64` |  | cleared at allocation |
| `+0x18` | `u64` |  | cleared at allocation |
| `+0x20` | `u8` |  | 0 at allocation, `0xFF` from `0x002F4520` on every pass it does not refuse |
| `+0x21` | `-` |  | never written |

```
GS model constants
memory     0x100000 words   4 MiB
page       0x800 words      8 KiB, the budget's rounding unit
block      0x40 words       256 bytes, the unit of 0x02CA5FF4
surface    512 x 448 x 4 B  112 pages; three reserved = 688,128 words
```

Access tables beside this page:

| Subject | Table |
|---|---|
| the bound map's fields | [`legacy-ps2-gs-layer-legacy-ps2gs-texture-context-accesses.tsv`](legacy-ps2-gs-layer-legacy-ps2gs-texture-context-accesses.tsv) |
| texture records | [`legacy-ps2-gs-layer-legacy-ps-2-gs-source-texture-record-accesses.tsv`](legacy-ps2-gs-layer-legacy-ps-2-gs-source-texture-record-accesses.tsv) |
| instance records | [`legacy-ps2-gs-layer-legacy-ps-2-gs-reference-descriptor-accesses.tsv`](legacy-ps2-gs-layer-legacy-ps-2-gs-reference-descriptor-accesses.tsv) |
| slot records | [`legacy-ps2-gs-layer-legacy-ps-2-gs-derived-slot-record-accesses.tsv`](legacy-ps2-gs-layer-legacy-ps-2-gs-derived-slot-record-accesses.tsv) |
| `0x02064B00` | [`legacy-ps2-gs-layer-vu1-register-bank-02064b00-accesses.tsv`](legacy-ps2-gs-layer-vu1-register-bank-02064b00-accesses.tsv) |
| `0x01E02830` | [`legacy-ps2-gs-layer-vu-1c-onstant-vector-01e02830-accesses.tsv`](legacy-ps2-gs-layer-vu-1c-onstant-vector-01e02830-accesses.tsv) |
| `0x02064E30` | [`legacy-ps2-gs-layer-vu-1da-ta-memory-02064e30-accesses.tsv`](legacy-ps2-gs-layer-vu-1da-ta-memory-02064e30-accesses.tsv) |

</details>

## State

<details>
<summary>Show the state it keeps</summary>

| Address | What |
|---|---|
| `0x022D8EAC`, `0x022D8EB0`, `0x022D8EB4` | the 512 × 448 GS frame |
| `0x022D8EA8`, `0x022D8EB8` | frame index and pages per surface |
| `0x02CA5FF0`, `0x02CA5FF4` | `0x4000` and the reservation in blocks |
| `0x02CA6004`, `0x02CA6008` | the rebuild's largest footprint and weighted count |
| `0x0209A670`, `0x0209A6E8`, `0x0209A708` | bound map, weather slot, dirty word |

`0x0209A6F8` switches the map's draw. Each world step `0x0026EB30` copies it into the bound map's `+0x120`¹, the word `0x0026E290` tests before it draws the map ([when the rebuild
runs](#when-the-rebuild-runs)). Opcode `0x0B` of the battle effect program `0x003B8670` sets it and the screen-clear
switch `0x022D8EDC` to 0 before it files its light. Opcode `0x0A` and `0x0024D9C0` set both back to 1
([effect file loading](effect-file-loading.md)).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0026ED4E`-`0x0026ED54` |

</details>

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x0209A6F8` | `u32` | 0 (zero-filled tail) | 1 lets the bound map draw, 0 keeps `0x0026E290` from drawing it; copied to the map's `+0x120` every world step | `0x0026E640`, 1 (`0x0026E6BA`); `0x0024D9C0`, 1 (`0x0024D9C6`); `0x003B8670`: opcode `0x0A`, 1 (`0x003B96B3`), opcode `0x0B`, 0 (`0x003B9730`) | `0x0026EB30` (`0x0026ED4E`) |

### The widget draw block

`0x00276430` fills the block at `0x0209AB90` for one widget draw: it first makes the matrix `0x0209AB90`-`0x0209ABCF` an
identity with `0x00203170` (`0x00276494`-`0x002764A5`, four 16-byte stores), then writes the fields below. The widget draw
`0x00274CB0` (from `0x00274CA0` and `0x004048E0`) reads them; it reads the matrix through `0x00202B70`, whose vector transform
`0x00217060` loads all sixteen elements¹. The two words `0x0209A760` and
`0x0209A764` belong to the same call. Every field is 0 at load (the zero-filled tail of `.data`).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00274F2E`-`0x00274F39`, `0x00274F65`-`0x00274F93` |

</details>

| Global | Field | Type | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x0209A760` | - | `f32` | the call's fifth argument `u`, as a float | `0x00276430` (`0x0027652E`) | `0x00274CB0`, subtracted from and added to the transformed corners' x (`0x00274FAE`, `0x00274FD7`, `0x00274FFF`, `0x00275028`, `0x00275050`, `0x0027507D`) |
| `0x0209A764` | - | `f32` | the sixth argument `v`, as a float | `0x00276430` (`0x00276541`) | `0x00274CB0`, the same for y (`0x00274FBF`, `0x00274FDF`, `0x00275010`, `0x00275030`, `0x00275061`, `0x00275085`) |
| `0x0209ABA4` | `+0x14` | `f32` | the matrix's y scale: `scale` | `0x00203170`, 1.0 (`0x00203181`, 16 bytes over `+0x10` to `+0x1F`); `0x00276430` (`0x002764D6`) | `0x00217060` (`0x002170A1`) |
| `0x0209ABC0` | `+0x30` | `f32` | the x offset: `2048 - [0x01E0C1D8] / 2 + x` | `0x00203170`, 0 (`0x00203197`, 16 bytes over `+0x30` to `+0x3F`); `0x00276430` (`0x0027651E`) | `0x00217060` (`0x002170AD`) |
| `0x0209ABC4` | `+0x34` | `f32` | the y offset: `2048 - [0x01E0C1DC] / 2 + y` | `0x00203170`, 0 (`0x00203197`); `0x00276430` (`0x00276539`) | `0x00217060` (`0x002170D8`) |
| `0x0209ABD0` | `+0x40` | `f32` | the rectangle's word `+0x08` | `0x00276430` (`0x00276608`) | `0x00274CB0` (`0x00274DDD`), scaled and truncated to an integer: `(i32)([0x0209ABD0] × 16.0)`, the factor 16.0 at `0x01CEBC84` (`0x00274DD2`-`0x00274DFA`) |
| `0x0209ABD4` | `+0x44` | `f32` | the rectangle's word `+0x0C` | `0x00276430` (`0x002765FB`) | `0x00274CB0` (`0x00274DFE`), the same |
| `0x0209ABD8` | `+0x48` | `f32` | the rectangle's word `+0x00` | `0x00276430` (`0x00276624`) | `0x00274CB0` (`0x00274DE5`), the same |
| `0x0209ABDC` | `+0x4C` | `f32` | the rectangle's word `+0x04` | `0x00276430` (`0x00276614`) | `0x00274CB0` (`0x00274E1A`), the same |
| `0x0209ABE0` | `+0x50` | `f32` | the widget's colour byte `+0x94` / 128 | `0x00276430` (`0x0027659D`) | `0x00274CB0` (`0x0027511D`) |
| `0x0209ABE4` | `+0x54` | `f32` | colour byte `+0x95` / 128 | `0x00276430` (`0x002765B0`) | `0x00274CB0` (`0x00275129`) |
| `0x0209ABE8` | `+0x58` | `f32` | colour byte `+0x96` / 128 | `0x00276430` (`0x002765CF`) | `0x00274CB0` (`0x00275146`) |
| `0x0209ABEC` | `+0x5C` | `f32` | colour byte `+0x97` / 128 | `0x00276430` (`0x002765D7`) | `0x00274CB0` (`0x0027513E`) |
| `0x0209ABF0` | `+0x60` | `f32` | `scale` × 8 | `0x00276430` (`0x0027661C`) | `0x00274CB0` (`0x002750C7`, `0x00275110`) |
| `0x0209ABF4` | `+0x64` | `f32` | the widget's float `+0x00` / 4096 | `0x00276430` (`0x00276567`) | `0x00274CB0` (`0x00274FC7`, `0x00275018`, `0x0027506D`) |
| `0x0209ABF8` | `+0x68` | `f32` | the widget's float `+0x14` / 4096 | `0x00276430` (`0x0027657F`) | `0x00274CB0` (`0x00274FCF`, `0x00275020`, `0x00275075`) |

### The display records, the surface entries and the other words

`0x0036D2F0` fills the two `0x28`-byte display records from a stack area that its call `0x0016D6A0`¹, a bare
`ret`, leaves as it was; it sets only bits `0x1FF` of the second record's word `+0x10` to the pages per surface². `0x022D8EA0` points at the first record³ or at record `[0x022D8EA8]`⁴;
no instruction loads that pointer.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0036D34E` |
| ² | `0x0036D399`-`0x0036D3A9` |
| ³ | `0x0036D3B2` |
| ⁴ | `0x0036D800` |

</details>

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x022D8E70` | `u64` | 0 | the first record's `+0x20`: the 8 bytes at the set-up's stack `+0x60` | `0x0036D2F0` (`0x0036D380`) | no instruction names it apart from that store; `0x0024DEE0` reads `+0x10` of a record only |
| `0x022D8E88` | `u8[16]` | 0 | the second record's `+0x10` to `+0x1F`: the stack bytes at `+0x78`, with bits `0x1FF` of the first dword set to 112, the pages per surface | `0x0036D2F0` (`0x0036D3C9`, 16 bytes) | `0x0024DEE0` (`0x0024DF8E`), the dword at `0x022D8E60` + `0x28` × `[0x022D8EA8]`, which is this one when the frame index is 1 |
| `0x022D8E98` | `u64` | 0 | the second record's `+0x20`: the stack bytes at `+0x88` | `0x0036D2F0` (`0x0036D3D0`) | no instruction names it apart from that store |
| `0x02AEECF8` | `u64` | 0 | the CLAMP value of the first surface entry: region clamp, maximum u = width − 1, v = height − 1; `0x0024B7B0` sets maximum u to 255 and maximum v to 223 in it (`0x0024B97C`-`0x0024B993`) | `0x0039D200` (`0x0039D29A`, in its loop over the first two entries from `0x02AEECF0`); `0x0024B7B0` (`0x0024B993`) | `0x0024B7B0` (`0x0024B97C`); `0x00431830` (`0x004318AB`), as entry `[+0xA8]` of `0x02AEE900 + 0x3F0` when that byte is 0 |
| `0x02AEED20` | `u64` | 0 | the TEX0 value of the fourth entry: `0x620110000` with base page `0x3700` | `0x0039D200` (`0x0039D2F3`, in its loop over the entries from `0x02AEED10` to `0x02AEED4F`, then `0x0039D3C2`) | `0x0039D200` (`0x0039D3AF`); the entry readers by index, entry 3: `0x00374280` (`0x00374349`), `0x003745C0` (`0x003746AB`) and `0x00375280` (`0x0037538C`) for a descriptor kind of 6 (they take kinds 3 to 6 as entries 0 to 3), `0x004FD4B0` (`0x004FDABB`) for a signed 3-bit index of 3, `0x00431830` (`0x00431896`) for a byte `+0xA8` of 3 |
| `0x02AEED30` | `u64` | 0 | the TEX0 value of the fifth entry: `0x620110000` with base page `0x3300` | `0x0039D200` (`0x0039D2F3`, then `0x0039D3DC`) | `0x0039D200` (`0x0039D3C9`); `0x00431830` (`0x00431896`) for a byte `+0xA8` of 4 |
| `0x02EBB6C0` | `u64` | 0 | zeroed at start-up beside `0x02EBB6C8` | `0x00467BB0` (`0x00467BDA`) | no instruction names it apart from that store |
| `0x01EEBAE8` | `u32` | 10000 (`0x2710`) | the last entry of the pass's draw list: the `u16` at `[map + 0x1E0 + 0x18 × pass]` + 2 × (count − 1), the count being the dword `+0x10` of that list (`0x002F4774`-`0x002F4785`), stored before `0x001808A0` on each pass that is not refused (`0x002F458B`-`0x002F45B9`) | `0x002F4520` (`0x002F4789`) | no instruction names it apart from that store |

`0x01EEBAE4` and `0x022BE7DC`, set together by `0x002F4510` (from `0x001D1660`), bound the record indices of a pass: an entry
is drawn only when it is not below `0x022BE7DC` and not above `0x01EEBAE4`, both signed compares¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002F4906`-`0x002F491E` |

</details>

The effect-texture placer `0x002D83B0` (called at `0x00501285` and `0x00501405`) keeps its textures in the `0x10`-byte
entries of the block at `0x02F8DA00`. It walks the entries from the first while each starts no more than one unit past
the end of the one before, counting them¹. At the first empty entry it returns -1 when that
end equals `[0x02F8F200]`²; otherwise it raises `0x0215E6B0` to the count³ and places the texture there.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002D8410`-`0x002D843A` |
| ² | `0x002D847B`-`0x002D8486`, `0x002D850F` |
| ³ | `0x002D848C`-`0x002D8494` |

</details>

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x0215E6B0` | `i32` | 0 (zero-filled tail of `.data`) | the largest number of entries `0x002D83B0` has walked before placing a texture at the end of the run | `0x002D83B0` (`0x002D8494`, only when the count is greater, a signed compare) | `0x002D83B0` (`0x002D848C`), the compare before that store; no other RIP-relative instruction names it |
| `0x0215E6B4` | `i32` | 0 (zero-filled tail of `.data`) | the same for palettes: the largest number of entries the palette placer `0x002D81D0` has walked in the `0x10`-byte entries from `0x02F8C200` before placing a palette at the end of the run | `0x002D81D0` (`0x002D82C7`, only when the count is greater, a signed compare) | `0x002D81D0` (`0x002D82B6`), the compare before that store; no other RIP-relative instruction names it |

</details>

## Modding notes

- The texture budget is the same on every machine: 176 GS pages less the rebuild's two totals,
  rounded up to a page.
- A texture used by only one instance record never gets a slot, whatever the budget.
- Admission follows the bank order of the texture records; moving a large texture later in the bank
  lets smaller ones before it in.
- To refresh the slots, change the weather slot through `0x0026E8D0`; the next draw rebuilds. Calling
  `0x002F7380` directly skips the dirty bookkeeping.
- Bytes `+0x21` to `+0x27` of a slot record are never initialised; do not read them.

## Related

- [PS2 VIF1 and VU1 emulation](../Engine-Core/ps2-vif1-vu1-emulation.md): the VIF1 decoder, the microprograms, VU memory and the GS replay.
- [Graphics thread handshake](graphics-thread-handshake.md): the GS register batch that uses the surfaces.
- [Weather](../World-Areas-And-Travel/weather.md): the slot change that marks the map dirty.
- [MPK map pack](../World-Areas-And-Travel/mpk-map-pack.md): the map sections the texture and instance records come from.
- [Gi render commands](gi-render-commands.md): `GiPolyGT4T`'s texture-descriptor lookup.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 3 calls with 3 other topics</summary>

**Gameplay** (explained on [battle locomotion](../Movement-And-Pathfinding/battle-locomotion.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00203170`](legacy-ps2-gs-layer.md) | is called by | [`0x00339630`](../Battle-Actions/action-phases.md) (on action phases) |

**Game files and data tables** (explained on [debug menu](../Engine-Core/debug-menu.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x001D1660`](../Engine-Core/debug-menu.md) (on debug menu) | calls | [`0x002EEEE0`](../Engine-Core/debug-menu.md) (on debug menu) |

**Scripts and script commands**

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00203170`](legacy-ps2-gs-layer.md) | is called by | [`0x00356160`](effect-anchors-and-targets.md) (on effect anchors and targets) |

</details>
