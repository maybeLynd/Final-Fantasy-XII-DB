---
title: "Legacy PS2 GS layer: the GS memory model, the map texture slot rebuild and the VU register leftovers"
kind: "system"
category: "Graphics"
addresses: "0x0036D280, 0x0036D2F0, 0x022D8EAC, 0x022D8EB4, 0x022D8EA8, 0x003A1E50, 0x00466190, 0x00466220, 0x00467AA0, 0x00467AD0, 0x00467B00, 0x00467B10, 0x002F7380, 0x0026E290, 0x0026E8D0, 0x0209A670, 0x0209A6E8, 0x0209A708, 0x002F4520, 0x00244200, 0x004B9870, 0x01E02830, 0x02064B00"
---

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
`0x0036D290` are the only stores that name the three dimension words and the frame index.

`0x0036D2F0` then computes the pages per surface, `(width × height) >> 11` = 112 GS pages of 2,048
words, into `0x022D8EB8` (`0x0036D393`), fills the two 0x28-byte display records at `0x022D8E50` and
`0x022D8E78`, and points `0x022D8EA0` at the first. The GS register batch `0x0036D400` places the colour
surface at page `index × 112` with PSM 0 and the Z surface at page 224 with bit 24 set
([graphics thread handshake](graphics-thread-handshake.md)). With the index at 0 the frame uses
surfaces 0 and 2 of the three the budget reserves.

### GS page geometry

`0x003A1E50(width, height, psm)` returns a texture's footprint in 32-bit words, rounded up to whole
GS pages: `((height + ha - 1) & ~(ha - 1)) x ((width + wa - 1) & ~(wa - 1)) / d`, with the width align `wa`,
height align `ha` and divisor `d` of the table below (`0x003A1EBA`-`0x003A1ED8`).
It indexes the 43-byte table `0x003A1EF0` with `psm − 2`; an index above `0x2A`, which
includes PSM 0 and 1 through the unsigned compare at `0x003A1E68`, takes the default class. The
class picks an arm from `0x003A1EE0`:

| Class | PSMs | Width align | Height align | Divisor | Smallest footprint |
|---|---|---:|---:|---:|---:|
| default (`0x003A1EBA`) | all others, including `0x00`, `0x01` | 64 | 32 | 1 | 2,048 words |
| 0 (`0x003A1E96`) | `0x02`, `0x0A` | 64 | 64 | 2 | 2,048 words |
| 1 (`0x003A1E9E`) | `0x13`, `0x1B` | 128 | 64 | 4 | 2,048 words |
| 2 (`0x003A1EAD`) | `0x14`, `0x24`, `0x2C` | 128 | 128 | 8 | 2,048 words |

These are the GS page sizes of the 32-, 16-, 8- and 4-bit pixel formats. `0x00466190(bank, index)`
sums `0x003A1E50` over a texture record's mip levels, halving width and height each level, with the
level count at `+0x05` capped at 7 (`0x004661C5`–`0x004661CC`). `0x00466220(record)` returns 1 exactly for
PSMs `0x14`, `0x24` and `0x2C`: `(psm − 0x14) & 0xE7` must be 0 and `psm` must not be `0x1C`.

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

Each pass of the slot handler `0x002F4520` starts with `0x00467A70` (`0x002F45D9`), which sets the
cursor `0x02CA5FF8` back to the reservation `0x02CA5FF4` and zeroes `0x02CA5FFC` and `0x02CA6000`;
`0x00467A90` returns the cursor.

`0x002D7FC0`, run by the frame set-up `0x0024D540`, clears the two `0x1800`-byte blocks at `0x02F8DA00` and
`0x02F8C200`, keeps the width `0x022D8EAC` at `0x02F8F214` and places five block addresses after the surfaces,
moving them up by `(width - 0x200) x 0x540 / 64` for a width above `0x200` (0 at the shipped 512):

| Address | Type | Name | Meaning |
|---|---|---|---|
| `0x02F8F200` | `= 0x3B00` | 0x02F8F204 = 0x2A00 + d | `0x02F8F208` = `0x3C00` + d |
| `0x02F8F20C` | `=` | 0x3B00 | + d `0x02F8F210` = `0x3C00` + d |

### The surfaces as textures

`0x0039D200`, run by the same frame set-up (`0x0024D560`), rewrites six 16-byte entries at `0x02AEECF0`, each
a pair of values in the layout of the GS registers TEX0 and CLAMP, for draws that sample the surfaces:

| Entries | TEX0 value | CLAMP value | Base page (TEX0 bits 0-13) |
|---|---|---|---|
| `0x02AEECF0`, `0x02AEED00` | `0x664100000` with `width / 64` in bits 14-19: PSM 1, 512 × 512, TCC 1 | `10` (region clamp in u and v), maximum u = width − 1, v = height − 1 | `width × height / 64` in one of the two, 0 in the other |
| `0x02AEED10` to `0x02AEED40` | `0x620110000`: PSM 1, 256 × 256, TCC 1 | `10` with half the width and height | `0x3C00`, `0x3700`, `0x3300`, `0x3FFF` |

The full-size base goes into the first entry when bits 0-8 of the FRAME_1 value `0x022D8EC8` are 0, and
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
`+0x58` into `+0x94`: `rgb = (byte +0x90..+0x92 x s16 +0x5A) >> 7` and `a = (byte +0x93 x s16 +0x58) >> 7`
(`0x0027643F`-`0x0027649F`).

The draw-list build `0x002F5550` calls it (`0x002F5AB0`) on a stack copy of the view block at
`0x02AED500` whose depths it has replaced by `0x003B40B0` results, and copies the matrix to `+0x80` of
each `0xE0`-byte record of the map's tag-24 array (`[+0x1D0]`, count `+0x220`).

The slot handler `0x002F4520` first calls `0x00467B60` (`0x002F4670`), which stores
`int(−16 × log2|20 − c|)` in the high dword of `0x02EBB6C8`, with `c` the float at `0x02AED570`, the
working camera's `+0x10`. `0x00467BB0` zeroes the same qword at start-up; these two stores are the only
instructions that name it.

### When the rebuild runs

The bound map is the object at `0x0209A670` ([MPK map pack](../World-Areas-And-Travel/mpk-map-pack.md)).
`0x0026E8D0(slot)`, the weather rebind ([weather](../World-Areas-And-Travel/weather.md)), stores the slot
at `0x0209A6E8` and sets the dirty word `0x0209A708` (`0x0026E8E7`); `0x0026E960` sets it too when a map
is bound (`0x0026E9B0`). These are its only two non-zero stores; the reset `0x0026E1D0` clears it. The stores of 1 at
`0x0026E221` and `0x0026E9A6` go to the neighbouring word `0x0209A6FC`.

The draw's pass-bit-0 block calls `0x0036F430` and `0x0036F450`, which call `0x0026E290` with 0 and 1.
While a map is bound and its `+0x120` is non-zero, `0x0026E290` runs `0x002F7380(map, [0x0209A668])` when
the dirty word is set and then clears it (`0x0026E2C4`, `0x0026E2C9`), and then calls the map's
`+0x130` handler with the pass. That handler is `0x002F4520`, installed by the map set-up
`0x002F6AB0` (`0x002F6B43`); it starts by setting `+0x00` of every slot record to 0 and `+0x20` to
`0xFF` (`0x002F45F0`–`0x002F4617`).

The map's file reaches the set-up through an eight-slot table at `0x02EBB820` (`0x38` bytes a slot:
`+0x00` the data, `+0x08` a count, `+0x10` a word set to 2, `+0x14` a name). The binders `0x0026E760`
and `0x0026E7D0`, both from `0x00378120`, register the data with `0x003EC9A0`, which takes the next free
slot from a round-robin cursor: `slot = [0x02EBB9E0]`, then `[0x02EBB9E0] = ([0x02EBB9E0] + 1) % 8`, repeated while
`slot` holds data, at most eight times; a free slot adds 1 to `0x02EBB9E4` (`0x003EC9A0`-`0x003ECA66`). It writes a
fixed placeholder name and returns the slot number.

The set-up `0x002F6AB0` stores the number at map `+0x168` and reads the
slot back with `0x003EC970(n)` (null past 7 or for an empty slot), keeping the data at `+0x158` and the
name at `+0x160`. The map teardown `0x002F5450` releases it with `0x003ECA70(n)`, which frees the data
when the count is positive (`0x003EC8A0`) and clears the slot.

`0x00862910` truncates a float vector to four integers, and `0x00862930` does the same after scaling by
16, the GS coordinate form. The model instance's draw setup `0x004FD4B0` converts the instance's
`+0xD0` with the first and writes the fourth integer into bits 56–63 of the GS FOG register
(`0x0A`); the point projector `0x00272180` and the map screen code `0x003C29A0` use the second.

### The slot rebuild

`0x002F7380(map)` works on the map's texture records (a bank at `[+0x150]`: count at `+0x00`,
0x60-byte records from `[+0x08]`) and its instance records (`[+0x178]`, 0x30 bytes, count `+0x174`):

1. free the old slot table at `+0x218` (`0x003EC8A0`) and copy the bank's count to `+0x224`;
2. for every texture record: track the largest mip-chain footprint (`0x00466190`, `0x002F7436`–`0x002F743B`),
   add 1 for a 4-bit record or 4 for any other to a second total (`0x002F744A`–`0x002F7455`), and set
   the word `+0x0E` to 0 (`0x002F7445`);
3. publish the largest footprint to `0x02CA6004` (`0x00467B10`) and the total to `0x02CA6008`
   (`0x00467B00`), then take the budget from `0x00467AA0`;
4. for every instance record whose flag word `+0x0C` has bit `23 + slot` set (`0x002F738E`–`0x002F7397`,
   `0x002F74C9`) and whose texture index `+0x04` is at most `0x3FFF`: unless the record repeats the
   previous one's texture index and byte `+0x1D`, increment `+0x0E` of that texture record and of
   every following record whose `+0x0C` word is non-zero (`0x002F7500`–`0x002F753D`);
5. walk the texture records in bank order: a record counted more than once is admitted when the
   running total plus its footprint stays below the budget (`0x002F75A2`), and gets the next slot
   number in `+0x0E`; every other record gets `0xFFFF` (`0x002F75B0`). A record that does not fit is
   skipped and the walk goes on, so a smaller record later in the bank can still be admitted;
6. with any admitted, store the count at `+0x228`, allocate `count × 40` bytes (`0x003EC8D0(6, …)`)
   at `+0x218`, and zero `+0x00`, `+0x08`, `+0x10`, `+0x18` and the byte `+0x20` of each record
   (`0x002F760B`–`0x002F761F`).

`0x003EC8D0` reports a failed allocation by passing `"out of memory!\n"` to `0x00862690`, which hands
it to `0x008620B0`, a body that returns at once; nothing is printed.

### GS image transfers

`0x00244200`, called from `0x002D2DB0`, writes GS register records for image transfers: BITBLTBUF
`0x50`, TRXPOS `0x51`, TRXREG `0x52` and TRXDIR `0x53` (`0x002442D2`–`0x00244332`), then TRXPOS, TRXREG
and TRXDIR again (`0x00244355`–`0x0024439C`). It reads the frame index and the height to place the
transfer. The GS replay honours none of these four registers.

`0x002443D0(widget, node)`, also called from `0x002D2DB0` (`0x002D2F30`), sets node `+0x38` bit 8, clears bits 9-13,
and stores at node `+0x30` a TEX0 word: the constant `0x40010333C` (base `0x333C`, format 1, TCC set) with the
buffer width `0x022D8EAC` / 64, TW the highest set bit of 2 x width - 1 (9 for the shipped `0x200`) and TH 5, from
`0x3F`. It then writes TEXA (`0x3B`) = `0x80` under one A+D GIF tag (`0x00248EB0`, `0x00248E10`).

`0x003A22A0(packet, base, format, width, height, data)` builds a whole upload into a packet. It opens an
A+D GIF tag (`0x003A2090`) and writes BITBLTBUF with the destination base in bits 32–45, the buffer
width from `0x003A1FE0` in bits 48–53 and the format in bits 56–61, then TRXPOS 0, TRXREG
`width, height` and TRXDIR 0, and closes the tag (`0x0024B150`). The image follows through
`0x003A21A0`, and a second A+D tag writes TEXFLUSH (`0x3F`).

The data size is `0x003A1F20(width, height, format) / 4` (`0x003A22E0`-`0x003A22EF`).
`0x003A1F20` takes `n = width x height` and returns `n x 3 / 2` for
formats `1` and `0x31`, `n / 2` for `2`, `0x0A`, `0x32` and `0x3A`, `n / 4` for `0x13` and `0x1B`, `n / 8` for
`0x14`, `0x24` and `0x2C`, and `n` otherwise (`0x003A1F20`-`0x003A1F8C`).

- `0x003A1FE0(width, format)` is the buffer width in 64-pixel units: the width rounded up to a
  multiple of 64, or to a multiple of 128 for the formats `0x13`, `0x14`, `0x1B`, `0x24` and `0x2C`
  (the 8-bit and 4-bit indexed ones), divided by 64.
- `0x003A21A0(packet, qwords, data)` splits the image into pieces of at most `0x4000` quadwords. Each
  piece is a DMA `cnt` tag with a VIF `DIRECTHL` of one quadword carrying an IMAGE-mode GIF tag for
  the piece, then a DMA `ref` tag with a second `DIRECTHL` that points at the piece's place in the
  data. `0x0024AF50` and `0x003EFDF0` call it directly.

`0x0039D0C0(mode, id, width, height, target, a, b)` copies the rendered frame into the target of a GS
texture id. With no target given it takes the id's own (`0x002D7FA0`), or a new one from `0x00182B40`
when the id has none. It closes an open scene around the copy (`0x001FBE30`, `0x001FBE50`, then
`0x001FBD80`), copies through `0x00182A60`, whose source the first argument picks (`0x00186910`), with a
mode of 0 to 3 chosen from `a` and `b` (`0x00376320`), and records a changed target for the id
(`0x002D7D90`). `0x00244200` calls it for id `0x333C` at
512 × 448; `0x003749F0`, `0x00376220` and `0x003A2BD0` are the others.

A texture word in the GS TEX0 layout comes from `0x002D8050(word, width, height, format)`. It keeps the
base in bits 0–13, which the caller sets, and writes the buffer width in 64-pixel units rounded up
(1 becomes 2) in bits 14–19, the format in bits 20–25, the power-of-two exponents of the width and
height in bits 26–29 and 30–33, and bit 34; bits 35 and 36 are cleared.

The exponent is
`0x002D8150(n)`, the smallest e with 2^e ≥ n, at most 10. The effect-texture placer `0x002D83B0` builds
its words this way. The way back is `0x002D7F20(e)`: 2^e for e up to 10, 0 above. The screen-effect
upload `0x00375B90` (kind 4) reads the width and height out of its word `+0x30` with it and passes
them, with the base and the format, to `0x003A22A0`.

A second exponent helper, `0x003666E0(n)`, returns log2 n for a power of two `n`; its two callers are `0x003649A0` and
`0x00474710`. `0x00474710` builds a GS sprite packet of register and value pairs, registers `0x3F`, `0x4C`, `0x06`
(TEX0) and `0x42` (ALPHA, value `0x44`) (`0x00474F95`-`0x00474FF5`), with the colour `0x80808080` (`0x0047502A`), and
divides its two texture coordinates by `1 << 0x003666E0` of each texture dimension (`0x00475044`, `0x00475066`).

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
| `0x002710C0(w, eop)` | writes the GIF tag: A+D (`0xE`), one register, the record count as NLOOP and `eop` in bit 15 |
| `0x00271100(w)` | writes an UNPACK header (`0x6C008000` with the count in bits 16 up) after three `0x10000000` |
| `0x00271050(w)` | writes a DIRECT header: `0x13000000` (FLUSHA), `0x10000000`, `0x50000000` with the count |
| `0x002712E0(w, src, ad)` | closes a DIRECT chunk of `src`, with an A+D end record `{0x8000, 0xE}` when `ad` is 1 |
| `0x00270FF0(w)`, `0x00271010(w, n)` | end the packet: when anything was written, advance the buffer's cursor and flip it (`0x003A1DB0`) |

Each closer computes its chunk's record count and passes the header to `0x0016D6A0`, a bare `ret`, so the
DMA tag in the first qword of every chunk header is never written.

The content helpers write fixed packets:

- `0x00271760(w, block, matrix, extra)` builds a 15-record chunk: an UNPACK header for 13 records
  (`0x6C0D8000`), the 13 constant records from `0x00276190`, and FLUSHA, MSCAL (`0x13000000`,
  `0x14000000`). The constants are the matrix, the matrix `0x02AEDDB0` ([scripted camera](scripted-camera.md)),
  four 2047.5 and four 1.0, the last replaced by `extra` when given.
- `0x00271720(w)` writes VIF BASE 0 and OFFSET `0x200` (`0x03000000`, `0x02000200`) into the record at
  the cursor. `0x002715A0(w, picture, row, half)` writes a picture bind there: A+D with CLAMP_1 = 5 and
  TEX0_1 from the picture's `+0x30`, the palette offset `(half + row × 2) × 2` in bits 37 up.
- Both, and `0x00271870(w, data, bytes)`, store back the cursor value they read and nothing between
  moves it, so the next write lands on the same records. `0x00271870` passes `bytes / 16` and `data`
  to `0x0016D6A0`, so it copies nothing.
- Three helpers write records at a plain pointer and return the pointer past them; the HUD's target rings
  and `+0x10F30` marks use them (`0x0028C620`, `0x003F7CC0`).
- `0x00271530(p, eop, flat)` writes a four-register A+D packet: TEST_1 `0x53001`, ALPHA_1 `0x44`,
  PRMODECONT 1 and PRIM `0x5C` (a textured, blended, shaded triangle strip), or `0x54` without shading
  when `flat` is non-zero.
- `0x00271650(p, picture, row, half, eop)` writes a two-register picture bind, CLAMP_1 = 5 and TEX0_1 from
  the picture's `+0x30` with the palette offset `(half + row x 2) x 2` in bits 37 up.
- `0x002716C0(p, end)` writes FLUSHA, NOP and a DIRECT header counting the records from `p + 0x10` to `end`.
- `0x002724A0(w)` ends a VU1 draw: the record at `[w + 0x38]` gets a GIF tag with end-of-packet, NLOOP
  `[w + 0x40]` and the registers ST, RGBAQ, XYZF2 (`0x412`); it completes the UNPACK header at
  `[w + 0x20]`, appends FLUSHA and MSCNT (`0x17000000`), closes the chunk and ends the packet.

- `0x00428980`, the last step of the character-record pass `0x004264A0` (from `0x00332440` and
  `0x00332510`), writes one DIRECT chunk into the current GS command buffer (`0x005044B0`): an A+D GIF tag
  with end-of-packet (`0x003A2090`), ZBUF_1 `0x4E` and ZBUF_2 `0x4F` from `0x022D8ED0`, FBA_1 `0x4A` = 0,
  TEST_1 `0x47` = `0x50000` (depth test, greater or equal) and ALPHA_1 `0x42` = `0x44`.
- `0x44` is the blend `(Cs − Cd) × As + Cd`. `0x003A2020` fills the tag's loop count, `0x00428980` gives
  the chunk header FLUSH and DIRECT with the record count, and `0x00504490` flips the buffer
  (`0x003A1DB0`).

### VU register words outside VU memory

Recompiled VU1 microprograms keep VU registers in fixed globals next to the emulated VU memory
`0x02064E30`:

- `0x02064B00` is a scratch cell shared by many recompiled programs from `0047xxxx` to `0054xxxx`, and
  by a few effect routines (`0x002F05F8`).
- One of its writers is the division helper `0x004B9870`, which stores `a / b`, or
  `0x7F7FFFFF` (`0x00900360`, the largest float) when `b` is 0. The programs `0x004B1190` and `0x004C8320`
  load its address six times each and pass it to `0x004B9870` four times (`0x004B7C31`, `0x004B7CE4`,
  `0x004B895F`, `0x004B8A12`): for those two programs it plays the VU's Q register.
- `0x01E02830` holds `(0, 0, 0, 1.0)`, the fixed contents of the VU's register vf00. `0x004B1190` loads
  its address 17 times as the second operand of its lane helpers, which include `0x004B9D80`,
  `0x004B9E60` and `0x004B9A10`. `0x0022CC20` writes those four words again; 63 functions call it.
- `0x004ADD10`, another installed program, reads VU memory cells directly through `0x02064E30`.

- Two shared subroutines of the recompiled programs work on the register cell `0x02064CB0`.
  `0x005375F0` (12 callers, `0x004758E0` among them) reduces its x lane by whole turns of 2π, using
  `1 / 2π` (0.15915494) and π. `0x005376D0` (13 callers) writes the sine and cosine of that lane to
  `0x02064CC0` and `0x02064CC4`.
- `0x005376D0` first folds the angle into `[−π/2, π/2]` and then sums the odd powers up to the ninth
  with the coefficients −0.16666657, 0.0083330255, −0.00019807414 and 2.601887e-06. Its
  comparisons go through `0x005379D0(flags, vector, value)`, which builds a VU MAC flag word: bits 7
  to 4 for the lanes x to w below the value, bits 3 to 0 for the lanes equal to it.

## Layouts

Texture record (map +`0x150` bank, from [+`0x08`]), `0x60` bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | psm | GS pixel format |
| `+0x05` | `u8` | levels | capped at 7 by `0x00466190` |
| `+0x06` | `u16` | width | halved per level |
| `+0x08` | `u16` | height | halved per level |
| `+0x0C` | `u16` | continues | non-zero: counted with the record before it |
| `+0x0E` | `i16` | count, then slot | reference count during step 4; slot or `0xFFFF` after step 5 |

Instance record (map +`0x178`, tag 30 of the map pack), `0x30` bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x02` | `i16` | placement row | read by `0x003A6FC0` |
| `+0x04` | `u16` | texture record index |  |
| `+0x0C` | `u32` | flags | bit 23 + slot: present for that weather slot |
| `+0x1D` | `u8` | sub-index | a repeat of the previous index and sub-index is not counted again |

Slot record (map +`0x218`, count +`0x228`), `0x28` bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u64` | cleared at allocation and by 0x002F4520 every pass |  |
| `+0x08` | `u64` | cleared at allocation |  |
| `+0x10` | `u64` | cleared at allocation |  |
| `+0x18` | `u64` | cleared at allocation |  |
| `+0x20` | `u8` | 0 at allocation, 0xFF from 0x002F4520 every pass |  |
| `+0x21` | `-` | never written |  |

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
| the bound map's fields | `legacy-ps2-gs-layer-legacy-ps2gs-texture-context-accesses.tsv` |
| texture records | `legacy-ps2-gs-layer-legacy-ps-2-gs-source-texture-record-accesses.tsv` |
| instance records | `legacy-ps2-gs-layer-legacy-ps-2-gs-reference-descriptor-accesses.tsv` |
| slot records | `legacy-ps2-gs-layer-legacy-ps-2-gs-derived-slot-record-accesses.tsv` |
| `0x02064B00` | `legacy-ps2-gs-layer-vu1-register-bank-02064b00-accesses.tsv` |
| `0x01E02830` | `legacy-ps2-gs-layer-vu-1c-onstant-vector-01e02830-accesses.tsv` |
| `0x02064E30` | `legacy-ps2-gs-layer-vu-1da-ta-memory-02064e30-accesses.tsv` |

## State

| Address | What |
|---|---|
| `0x022D8EAC`, `0x022D8EB0`, `0x022D8EB4` | the 512 × 448 GS frame |
| `0x022D8EA8`, `0x022D8EB8` | frame index and pages per surface |
| `0x02CA5FF0`, `0x02CA5FF4` | `0x4000` and the reservation in blocks |
| `0x02CA6004`, `0x02CA6008` | the rebuild's largest footprint and weighted count |
| `0x0209A670`, `0x0209A6E8`, `0x0209A708` | bound map, weather slot, dirty word |

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
