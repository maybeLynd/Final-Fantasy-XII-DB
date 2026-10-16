---
title: "Graphics thread handshake: the shared command-state word, the GS register batch and the waits around them"
kind: "system"
category: "Graphics"
addresses: "02EBA3F8, 0036D400, 0036F360, 003A2D80, 003A2E30, 0036F2F0, 0036F2C0, 0036D7E0, 0022BFD0, 0035E9A0, 0035EC90, 00369100, 02EAF6D8, 003749F0, 00376050, 02F8F2E0, 00D10F88, 022D8EAC, 022D8EB4"
---

## What the player sees

Nothing directly. On the PlayStation 2 the game handed each frame's Graphics Synthesizer command
stream to the console's DMA hardware by writing a few registers, and waited for the hardware to
take it. The remaster keeps that code: every frame still builds the GS register batch, writes the
"kick" into one shared dword, spins until the dword settles and clears its bits. The waits finish at
once unless the vertical-sync thread's end-of-frame callback writes the word between two reads.

## How it works

### The word

`02EBA3F8` is one dword, zero in the image. Every instruction that names it is a plain load or
store: 24 stores (18 `mov`, 4 `and`, 2 `or`) and 38 loads, with no `lock` prefix anywhere. The
values that pass through it are successive values of one cell, not separate fields:

| Value or operation | Written by | Meaning on the PS2 path |
|---|---|---|
| buffer address `& 3FF0h`, then a record count | the three publishers | the start and length of a DMA chain |
| `100`<sub>h</sub> (bit 8) | the three publishers | the start bit, "batch published" |
| nine-store burst ending in 0 | the reset `0036F2F0` | the channel reset sequence |
| `and FFFFFEF3h` (bits 2, 3, 8 down) | the clear `0036F2C0` | batch accounted for |
| `or 10000h`, then `and FFFEFEFFh` | effect capture | capture bit up, then bits 8 and 16 down |
| 0 | `0036D7E0` | the vertical-sync callback's reset |

### The GS register batch

`0036D400(a, b)` builds the frame's GS environment ([Phyre frame](../PhyreEngine/the-frame.md)
lists its callers and the pass-mask bits that supply `a` and `b`). It reads the width `022D8EAC`
(512) and height `022D8EB4` (448), stores width / 2000.0 and height / 2000.0 at `022D8EF0` and
`022D8EF4` and 1.0 at `022D8EF8` and `022D8EFC`, and composes two register values:

- FRAME_1 at `022D8EC8`: frame index `[022D8EA8]` × pages per surface `[022D8EB8]`, with the
  buffer width `width >> 6` in bits 16 and up (`0036D477`–`0036D4B4`);
- ZBUF_1 at `022D8ED0`: twice the pages per surface, with bit 24 set (`0036D496`–`0036D4C2`).

It then writes into the current GS command buffer (`02EBEFC0` + `18`<sub>h</sub> × `[02EBEFF0]`, see
[render command list](render-command-list.md)), one 16-byte record `{value, register}` per register:

1. a header record reserved first and filled at the end;
2. an A+D GIF tag (`003A2090`, register list `E`<sub>h</sub>, end-of-packet bit);
3. FRAME_1 `4C`<sub>h</sub>, ZBUF_1 `4E`<sub>h</sub>, XYOFFSET_1 `18`<sub>h</sub> (`(1000h − w) × 8`, `(1000h − h) × 8`),
   SCISSOR_1 `40`<sub>h</sub> (0 to w−1, 0 to h−1), PRMODECONT `1A`<sub>h</sub> = 1, COLCLAMP `46`<sub>h</sub> = 1, DTHE `45`<sub>h</sub> = 0;
4. when the table entry `00D10F88[(a != 0) | (b != 0) << 1]` is non-zero: a screen clear (below);
5. TEST_1 `47`<sub>h</sub> = `50000`<sub>h</sub> (`0036D733`), and `003A2020` writes the tag's loop count.

The table holds 0, `32001`<sub>h</sub>, `31001`<sub>h</sub> and `30000`<sub>h</sub>; the chosen entry is the clear's TEST_1
value. The clear sets TEST_1, PRIM (register 0) = 6, a sprite, and RGBAQ (register 1) to the colour
`[022D8ED8]` when `[022D8EDC]` is non-zero, else 0; `003A20C0` then emits XYZ2 (register 4) pairs
that cover the screen in sprites 64 pixels wide.

The header record gets `(records − 1) | 10000000h` in its first qword (`0036D781`) and
`5000000011000000h | records << 32` in its second (`0036D792`): a DMA `cnt` tag followed by the
VIF codes FLUSH (`11`<sub>h</sub>) and DIRECT (`50`<sub>h</sub>) with the record count. `0036D400` ends with
`003A1DB0` (`0036D7AD` or `0036D7C7`), which flips the buffers and calls the first publisher.

### The three publishers

`0036F360(buffer, records)` returns at once for 0 records. When the last record's first dword has
`30000000`<sub>h</sub> under the mask `70000000`<sub>h</sub> (a DMA `ref` tag) it writes the `cnt` record
`{10000000h, 0}` after it, or over it when the buffer already holds `200`<sub>h</sub> records
(`0036F372`–`0036F39C`). Then:

1. it stores `buffer & 3FF0h` (`0036F3A6`) and the record count (`0036F3AC`) into the word;
2. it loads the word three times and compares the values as cursors, looping until they fit
   (`0036F3B2`–`0036F3E9`); all three loads return the count it just stored, so the loop ends on its first pass;
3. it stores `100`<sub>h</sub> (`0036F3EB`).

`003A2D80(source, bytes)` rounds the size down to whole 16-byte records, copies the batch with
`memcpy` (`00861EBA`) to the staging buffer `[02F8F2E0]` (set to the GS buffer arena base
`[01FD4A78]` by the display-list set-up at `003A371A`), tests the fence (below), flips bit 10 of
the staging pointer (`xor 400h`, `003A2DCB`), so two staging buffers alternate `400`<sub>h</sub> bytes
apart, and stores the address, the count, and after its guard loop `100`<sub>h</sub> (`003A2E16`). It is
called from `0044D80C`, `004537CE` and `00460F08`.

`003A2E30(source, bytes, pointer, bytes2)` does the same copy and appends two records by hand: a
`ref` record (`+3` = `30`<sub>h</sub>, `u16` count `bytes2 / 16`, `+4` the pointer as a 32-bit image address
through `0020E620`) and a `cnt` record (`+3` = `10`<sub>h</sub>, `+C`<sub>h</sub> = `0404`<sub>h</sub>, `+F`<sub>h</sub> = 1), then
publishes count + 2 (`003A2F59`). Its only route is the guard stub `0045BAD0`
(`cmp byte [rcx], 0` / `jne 0045BAE0`), called from `002F4020` at `002F42C2`.

The guard loops of `003A2D80` and `003A2E30` first wait for a non-zero word (`003A2DE1`–`003A2DE9`,
`003A2F10`–`003A2F18`). `003A2D80` stores `bytes / 16` as the count, so a call with fewer than 16
bytes stores 0 and that loop has nothing that ends it on the thread that runs it.

### The fence nothing writes

`02EAF6D8` is zero in the image and every one of its 17 references is a load, in nine functions.
Each is the hoisted form `mov eax, [02EAF6D8]; and eax, 100h; test eax, eax; jne` back to the
`test`, which never reloads. With the word at 0 every one falls through: `0036F2F0`'s at
`0036F300`, the publishers' at `003A2DC1` and `003A2EE8`, and the rest in `0024D370`, `00259030`,
`002590F0`, `003749F0`, `00375500` and `00376050`.

### The reset burst

`0036F2F0` runs at the start of every frame state (`0022A7E7`, `0022AF5E`, `0022B004`, `0022B6E4`,
`0022B7E6`, `0022B8ED`, `0022BC35`), again at `0022A87F` and `0022B2FD`, in the effect-capture
draw `003749F0` (`00374ACE` or `00374AD7`) and in `00376220`. After the fence it stores nine values with no branch between them
(`0036F30D`–`0036F352`): the low dword of the address `022D9B50`, `7FFF0`<sub>h</sub>, 0, the address twice,
`(word & ~4) | 8`, `word & ~30h`, `14D`<sub>h</sub>, and 0. No instruction in the image tests bits 2, 3, 4,
5 or the value `14D`<sub>h</sub>; the burst ends with the word at 0.

### The settle-spin and the clear

`0036F2C0` is nine instructions: load the word into `ecx`, load it into `eax`, compare, loop back
while they differ (`0036F2D0`–`0036F2DE`), then `and dword [02EBA3F8], FFFFFEF3h` (`0036F2E0`).
The loop repeats only when a store lands between the two loads. A decompiler folds the two loads
into one and shows only the `and`.

The same loop is inlined ten more times, all on this word:

| Loop | Function | Followed by |
|---|---|---|
| `0022A850` | `0022A770` (field frame) | `0036F2C0` at `0022A860` |
| `0022AE50` | `0022A770` (field frame) | `002E65A0`, then `0036F2C0` at `0022AE74` |
| `0022AFA0` | `0022AF50` | `0036F2C0` at `0022AFB0` |
| `0022B040` | `0022B000` | `0036F2C0` at `0022B050` |
| `0022B2C0` | `0022B0B0` (the draw) | `0036F2C0` at `0022B2D0` |
| `0022B720` | `0022B6E0` | `0036F2C0` at `0022B7A4` |
| `0022B820` | `0022B7E0` | `0036F2C0` at `0022B86B` |
| `0022BAD0` | `0022B8C0` (full menu) | `002E65A0`, then `0036F2C0` at `0022BAFE` |
| `0022BD20` | `0022BC20` | `002E65A0`, then `0036F2C0` at `0022BD4E` |
| `00262AE0` | `002628B0` | — |

Where a site calls `0036F2C0` afterwards, the wait runs twice.

### The vertical-sync callback

After its clear, each frame state hands `0022BFD0` to `0035E9A0` (`0022AE7E` in the field frame,
and in `0022B6E0`, `0022B7E0`, `0022B8C0`, `0022BC20`), which stores it at `022CA5C8`. The
vertical-sync set-up `0035E820` registers `0035EC90` as handler 0 with `00369070` (`0035E93A`), and
the thread body `00369100` (created by `00368DD0` under the name `TkSyncvThread%d`) waits on its
event and calls the handlers in the table `022CFF10`.

`0035EC90` counts vertical syncs in `022CA5F0`. When the count reaches `022CA5F4` and its mode
test passes it sets `022CA600` (`0035ECFE`); while `022CA600` is set it calls the pending callback
and clears `022CA5C8` (`0035ED12`–`0035ED20`). The callback `0022BFD0` runs
`00368A70` and then `0036D7E0`, which stores 0 in the word (`0036D7E7`) and points `022D8EA0` at
the `28`<sub>h</sub>-byte display record `022D8E50 + 28h × [022D8EA8]`. This store comes from the TkSyncv
thread, so a settle-spin on the frame thread can see the word change between its two loads.

### Effect capture

The capture draws `003749F0` and `00376050` wait while bit 8 is set with a loop that reloads the
word (`00374C70`–`00374C7A`, `003761E0`–`003761EA`), then `or` `10000`<sub>h</sub> and immediately `and`
`FFFEFEFF`<sub>h</sub> (`00374CEC`/`00374CF6`, `003761EC`/`003761F6`), so the capture bit is up for one
instruction and the `and` also drops bit 8.

## Layouts

```
command-state word 02EBA3F8, as the PS2 code uses it
  publish   word = buffer & 0x3FF0 ; word = records ; word = 0x100
  clear     word &= 0xFFFFFEF3          bits 2, 3, 8
  capture   word |= 0x10000 ; word &= 0xFFFEFEFF
  reset     nine stores ending in 0 (0036F2F0); 0 (0036D7E0)
```

GS command record, `10`<sub>h</sub> bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u64` | value |  |
| `08`<sub>h</sub> | `u64` | register | GS register number; the header and GIF tag records hold tags |

GS environment globals (seeded by `0036D280`):

| Address | Type | Name | Meaning |
|---|---|---|---|
| `022D8EA8` | `u32` | frame index | 0 |
| `022D8EAC` | `u32` | width | `200`<sub>h</sub> |
| `022D8EB0` | `u32` | display width | `200`<sub>h</sub>, read as a u16 by `0036D2F0` |
| `022D8EB4` | `u32` | height | `1C0`<sub>h</sub> |
| `022D8EB8` | `u32` | pages/surface | (width * height) >> 11 = 112 (`0036D2F0`) |
| `022D8EC8` | `u64` | FRAME_1 value |  |
| `022D8ED0` | `u64` | ZBUF_1 value |  |
| `022D8ED8` | `u32` | clear colour |  |
| `022D8EDC` | `u32` | clear colour on 1 |  |
| `022D8EF0` | `f32` | width / 2000 | `022D8EF4`  f32  height / 2000 |

The spin census is beside this page in `graphics-thread-handshake-inert-spin-census.tsv`: every
backward loop in 38,161 listed bodies whose body only tests registers, 19 in all. Seventeen are the
fence tests above. The other two wait for a latch that is loaded once outside the loop: `00560A60`
in `00560910` on `02CA8F94` and `00566163` in `00565E00` on `02CA96D4`. Each latch is set to 1 only
by an 11-byte callback (`00556560`, `00563550`), so each loop either falls through or never ends.

## State

| Address | What |
|---|---|
| `02EBA3F8` | the command-state word |
| `02EAF6D8` | the fence, never written |
| `02F8F2E0` | the staging pointer of `003A2D80` and `003A2E30` |
| `022CA5C8` | the pending end-of-frame callback |
| `022CFF10` | the TkSyncv handler table |
| `022D8EA0`, `022D8E50` | the current display record and the record array |

## Modding notes

- Read this code from disassembly: the decompiler removes all eleven settle-spins.
- The publishers store `100`<sub>h</sub> with a plain `mov`, so any bit a hook sets in the word is lost at
  the next publish.
- A hook that blocks inside a settle-spin burns the core; the waits are loops, not sleeps.
- Do not call `003A2D80` with fewer than 16 bytes.
- The batch's FRAME, SCISSOR, XYOFFSET, PRMODECONT, COLCLAMP and DTHE settings are not honoured by
  the GS replay ([PS2 VIF1 and VU1 emulation](../Engine-Core/ps2-vif1-vu1-emulation.md));
  the register list there is the one that reaches the PC renderer.

## Related

- [Render command list](render-command-list.md): the two GS command buffers and the object list.
- [Phyre frame](../PhyreEngine/the-frame.md): the draw that calls `0036D400` and its pass mask.
- [PS2 VIF1 and VU1 emulation](../Engine-Core/ps2-vif1-vu1-emulation.md): the GIF tag and the GS replay.
- [Frame update order](../Engine-Core/frame-update-order.md): the frame states and the end-of-frame group.
- [Legacy PS2 GS layer](legacy-ps2-gs-layer.md): the 512 × 448 surfaces the batch addresses.
