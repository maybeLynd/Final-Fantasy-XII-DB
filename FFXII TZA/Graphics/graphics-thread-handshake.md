---
title: "Graphics thread handshake: the shared command-state word, the GS register batch and the waits around them"
kind: "system"
category: "Graphics"
addresses: "0x02EBA3F8, 0x0036D400, 0x0036F360, 0x003A2D80, 0x003A2E30, 0x0036F2F0, 0x0036F2C0, 0x0036D7E0, 0x0022BFD0, 0x0035E9A0, 0x0035EC90, 0x00369100, 0x02EAF6D8, 0x003749F0, 0x00376050, 0x02F8F2E0, 0x00D10F88, 0x022D8EAC, 0x022D8EB4"
---

## What the player sees

Nothing directly. On the PlayStation 2 the game handed each frame's Graphics Synthesizer command
stream to the console's DMA hardware by writing a few registers, and waited for the hardware to
take it. The remaster keeps that code: every frame still builds the GS register batch, writes the
"kick" into one shared dword, spins until the dword settles and clears its bits. The waits finish at
once unless the vertical-sync thread's end-of-frame callback writes the word between two reads.

## How it works

### The word

`0x02EBA3F8` is one dword, zero in the image. Every instruction that names it is a plain load or
store: 24 stores (18 `mov`, 4 `and`, 2 `or`) and 38 loads, with no `lock` prefix anywhere. The
values that pass through it are successive values of one cell, not separate fields:

| Value or operation | Written by | Meaning on the PS2 path |
|---|---|---|
| buffer address `& 0x3FF0`, then a record count | the three publishers | the start and length of a DMA chain |
| `0x100` (bit 8) | the three publishers | the start bit, "batch published" |
| nine-store burst ending in 0 | the reset `0x0036F2F0` | the channel reset sequence |
| `and 0xFFFFFEF3` (bits 2, 3, 8 down) | the clear `0x0036F2C0` | batch accounted for |
| `or 0x10000`, then `and 0xFFFEFEFF` | effect capture | capture bit up, then bits 8 and 16 down |
| 0 | `0x0036D7E0` | the vertical-sync callback's reset |

### The GS register batch

`0x0036D400(a, b)` builds the frame's GS environment ([Phyre frame](../PhyreEngine/the-frame.md)
lists its callers and the pass-mask bits that supply `a` and `b`). It reads the width `0x022D8EAC`
(512) and height `0x022D8EB4` (448), stores width / 2000.0 and height / 2000.0 at `0x022D8EF0` and
`0x022D8EF4` and 1.0 at `0x022D8EF8` and `0x022D8EFC`, and composes two register values:

- FRAME_1 at `0x022D8EC8`: frame index `[0x022D8EA8]` × pages per surface `[0x022D8EB8]`, with the
  buffer width `width >> 6` in bits 16 and up (`0x0036D477`–`0x0036D4B4`);
- ZBUF_1 at `0x022D8ED0`: twice the pages per surface, with bit 24 set (`0x0036D496`–`0x0036D4C2`).

It then writes into the current GS command buffer (`0x02EBEFC0` + 0x18 × `[0x02EBEFF0]`, see
[render command list](render-command-list.md)), one 16-byte record `{value, register}` per register:

1. a header record reserved first and filled at the end;
2. an A+D GIF tag (`0x003A2090`, register list `0xE`, end-of-packet bit);
3. FRAME_1 `0x4C`, ZBUF_1 `0x4E`, XYOFFSET_1 `0x18` (`(0x1000 − w) × 8`, `(0x1000 − h) × 8`),
   SCISSOR_1 `0x40` (0 to w−1, 0 to h−1), PRMODECONT `0x1A` = 1, COLCLAMP `0x46` = 1, DTHE `0x45` = 0;
4. when the table entry `0x00D10F88[(a != 0) | (b != 0) << 1]` is non-zero: a screen clear (below);
5. TEST_1 `0x47` = `0x50000` (`0x0036D733`), and `0x003A2020` writes the tag's loop count.

The table holds 0, `0x32001`, `0x31001` and `0x30000`; the chosen entry is the clear's TEST_1
value. The clear sets TEST_1, PRIM (register 0) = 6, a sprite, and RGBAQ (register 1) to the colour
`[0x022D8ED8]` when `[0x022D8EDC]` is non-zero, else 0; `0x003A20C0` then emits XYZ2 (register 4) pairs
that cover the screen in sprites 64 pixels wide.

The header record gets `(records − 1) | 0x10000000` in its first qword (`0x0036D781`) and
`0x5000000011000000 | records << 32` in its second (`0x0036D792`): a DMA `cnt` tag followed by the
VIF codes FLUSH (`0x11`) and DIRECT (`0x50`) with the record count. `0x0036D400` ends with
`0x003A1DB0` (`0x0036D7AD` or `0x0036D7C7`), which flips the buffers and calls the first publisher.

### The three publishers

`0x0036F360(buffer, records)` returns at once for 0 records. When the last record's first dword has
`0x30000000` under the mask `0x70000000` (a DMA `ref` tag) it writes the `cnt` record
`{0x10000000, 0}` after it, or over it when the buffer already holds `0x200` records
(`0x0036F372`–`0x0036F39C`). Then:

1. it stores `buffer & 0x3FF0` (`0x0036F3A6`) and the record count (`0x0036F3AC`) into the word;
2. it loads the word three times and compares the values as cursors, looping until they fit
   (`0x0036F3B2`–`0x0036F3E9`); all three loads return the count it just stored, so the loop ends on its first pass;
3. it stores `0x100` (`0x0036F3EB`).

`0x003A2D80(source, bytes)` rounds the size down to whole 16-byte records, copies the batch with
`memcpy` (`0x00861EBA`) to the staging buffer `[0x02F8F2E0]` (set to the GS buffer arena base
`[0x01FD4A78]` by the display-list set-up at `0x003A371A`), tests the fence (below), flips bit 10 of
the staging pointer (`xor 0x400`, `0x003A2DCB`), so two staging buffers alternate `0x400` bytes
apart, and stores the address, the count, and after its guard loop `0x100` (`0x003A2E16`). It is
called from `0x0044D80C`, `0x004537CE` and `0x00460F08`.

`0x003A2E30(source, bytes, pointer, bytes2)` does the same copy and appends two records by hand: a
`ref` record (`+3` = `0x30`, `u16` count `bytes2 / 16`, `+4` the pointer as a 32-bit image address
through `0x0020E620`) and a `cnt` record (`+3` = `0x10`, `+0xC` = `0x0404`, `+0xF` = 1), then
publishes count + 2 (`0x003A2F59`). Its only route is the guard stub `0x0045BAD0`
(`cmp byte [rcx], 0` / `jne 0x0045BAE0`), called from `0x002F4020` at `0x002F42C2`.

The guard loops of `0x003A2D80` and `0x003A2E30` first wait for a non-zero word (`0x003A2DE1`–`0x003A2DE9`,
`0x003A2F10`–`0x003A2F18`). `0x003A2D80` stores `bytes / 16` as the count, so a call with fewer than 16
bytes stores 0 and that loop has nothing that ends it on the thread that runs it.

### The fence nothing writes

`0x02EAF6D8` is zero in the image and every one of its 17 references is a load, in nine functions.
Each is the hoisted form `mov eax, [0x02EAF6D8]; and eax, 0x100; test eax, eax; jne` back to the
`test`, which never reloads. With the word at 0 every one falls through: `0x0036F2F0`'s at
`0x0036F300`, the publishers' at `0x003A2DC1` and `0x003A2EE8`, and the rest in `0x0024D370`, `0x00259030`,
`0x002590F0`, `0x003749F0`, `0x00375500` and `0x00376050`.

### The reset burst

`0x0036F2F0` runs at the start of every frame state (`0x0022A7E7`, `0x0022AF5E`, `0x0022B004`, `0x0022B6E4`,
`0x0022B7E6`, `0x0022B8ED`, `0x0022BC35`), again at `0x0022A87F` and `0x0022B2FD`, in the effect-capture
draw `0x003749F0` (`0x00374ACE` or `0x00374AD7`) and in `0x00376220`. After the fence it stores nine values with no branch between them
(`0x0036F30D`–`0x0036F352`): the low dword of the address `0x022D9B50`, `0x7FFF0`, 0, the address twice,
`(word & ~4) | 8`, `word & ~0x30`, `0x14D`, and 0. No instruction in the image tests bits 2, 3, 4,
5 or the value `0x14D`; the burst ends with the word at 0.

### The settle-spin and the clear

`0x0036F2C0` is nine instructions: load the word into `ecx`, load it into `eax`, compare, loop back
while they differ (`0x0036F2D0`–`0x0036F2DE`), then `and dword [0x02EBA3F8], 0xFFFFFEF3` (`0x0036F2E0`).
The loop repeats only when a store lands between the two loads. A decompiler folds the two loads
into one and shows only the `and`.

The same loop is inlined ten more times, all on this word:

| Loop | Function | Followed by |
|---|---|---|
| `0x0022A850` | `0x0022A770` (field frame) | `0x0036F2C0` at `0x0022A860` |
| `0x0022AE50` | `0x0022A770` (field frame) | `0x002E65A0`, then `0x0036F2C0` at `0x0022AE74` |
| `0x0022AFA0` | `0x0022AF50` | `0x0036F2C0` at `0x0022AFB0` |
| `0x0022B040` | `0x0022B000` | `0x0036F2C0` at `0x0022B050` |
| `0x0022B2C0` | `0x0022B0B0` (the draw) | `0x0036F2C0` at `0x0022B2D0` |
| `0x0022B720` | `0x0022B6E0` | `0x0036F2C0` at `0x0022B7A4` |
| `0x0022B820` | `0x0022B7E0` | `0x0036F2C0` at `0x0022B86B` |
| `0x0022BAD0` | `0x0022B8C0` (full menu) | `0x002E65A0`, then `0x0036F2C0` at `0x0022BAFE` |
| `0x0022BD20` | `0x0022BC20` | `0x002E65A0`, then `0x0036F2C0` at `0x0022BD4E` |
| `0x00262AE0` | `0x002628B0` | — |

Where a site calls `0x0036F2C0` afterwards, the wait runs twice.

### The vertical-sync callback

After its clear, each frame state hands `0x0022BFD0` to `0x0035E9A0` (`0x0022AE7E` in the field frame,
and in `0x0022B6E0`, `0x0022B7E0`, `0x0022B8C0`, `0x0022BC20`), which stores it at `0x022CA5C8`.

The vertical-sync set-up `0x0035E820` registers `0x0035EC90` as handler 0 with `0x00369070` (`0x0035E93A`), and
the thread body `0x00369100` (created by `0x00368DD0` under the name `TkSyncvThread%d`) waits on its
semaphore `[0x022CFEEC + 4n]` (`0x00369128`), calls handler n of the table `0x022CFF10` (`0x0036913A`) and then,
unless `0x0017D3E0` reports the debug byte `+0xD07` of `[0x001D50D0()]` set, releases the next semaphore
`[0x022CFEF0 + 4n]` (`0x0036914D`), without end.

`0x0035EC90` counts vertical syncs in `0x022CA5F0`. When the count reaches `0x022CA5F4` and its mode
test passes it sets `0x022CA600` (`0x0035ECFE`); while `0x022CA600` is set it calls the pending callback
and clears `0x022CA5C8` (`0x0035ED12`–`0x0035ED20`).

On every call `0x0035EC90` also increments the tick counter `0x022CA5E0`
(and `0x022CA5E8` while `0x022CA5FC` is 0), polls the input channels through `0x0035FCA0` (`0x0035ED2B`), and ends by
tail-jumping to `0x003690F0` (`0x0035ED34`), which releases the semaphore `[0x022D7F90]` (`0x00863800`) that
`0x00369170` waits on.

The callback `0x0022BFD0` runs
`0x00368A70` and then `0x0036D7E0`, which stores 0 in the word (`0x0036D7E7`) and points `0x022D8EA0` at
the 0x28-byte display record `0x022D8E50 + 0x28 × [0x022D8EA8]`. This store comes from the TkSyncv
thread, so a settle-spin on the frame thread can see the word change between its two loads.

### The thread and semaphore wrappers

The vertical-sync set-up and the Tk threads use a thin layer over the Windows calls:

- `0x008636E0(desc, name, arg)` makes a `crossThreadImpl` thread object of 0x28 bytes (`0x00863430`, the name
  "UnknownThread" when none is given), files its id under the name in `0x02EB37B8`, and `0x00863610(thread, arg)` stores
  the argument and starts it (`ResumeThread`; `0x0035E92A`, `0x00368D53`);
- `0x00863520(thread, p)` sets the priority `(32 - p) / 2` (`SetThreadPriority`; `0x00368C61`);
- `0x00863540(desc)` makes a semaphore from the descriptor's counts (`0x008632E0`, `CreateSemaphoreW`; `0x0035E8A7`);
  `0x00863800` releases it by one, `0x00863690(sem, ms)` waits on it (`WaitForSingleObject`), and `0x00863590` closes and
  frees it (`0x0035E74B`);
- `0x008635F0(ms)` sleeps (`0x0035E735`, `0x0035EAB3`).

### Effect capture

The capture draws `0x003749F0` and `0x00376050` wait while bit 8 is set with a loop that reloads the
word (`0x00374C70`–`0x00374C7A`, `0x003761E0`–`0x003761EA`), then `or` `0x10000` and immediately `and`
`0xFFFEFEFF` (`0x00374CEC`/`0x00374CF6`, `0x003761EC`/`0x003761F6`), so the capture bit is up for one
instruction and the `and` also drops bit 8.

## Layouts

```
command-state word 0x02EBA3F8, as the PS2 code uses it
  publish   word = buffer & 0x3FF0 ; word = records ; word = 0x100
  clear     word &= 0xFFFFFEF3          bits 2, 3, 8
  capture   word |= 0x10000 ; word &= 0xFFFEFEFF
  reset     nine stores ending in 0 (0x0036F2F0); 0 (0x0036D7E0)
```

GS command record, `0x10` bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u64` | value |  |
| `+0x08` | `u64` | register | GS register number; the header and GIF tag records hold tags |

GS environment globals (seeded by `0x0036D280`):

| Address | Type | Name | Meaning |
|---|---|---|---|
| `0x022D8EA8` | `u32` | frame index | 0 |
| `0x022D8EAC` | `u32` | width | `0x200` |
| `0x022D8EB0` | `u32` | display width | `0x200`, read as a u16 by `0x0036D2F0` |
| `0x022D8EB4` | `u32` | height | `0x1C0` |
| `0x022D8EB8` | `u32` | pages/surface | (width * height) >> 11 = 112 (`0x0036D2F0`) |
| `0x022D8EC8` | `u64` | FRAME_1 value |  |
| `0x022D8ED0` | `u64` | ZBUF_1 value |  |
| `0x022D8ED8` | `u32` | clear colour |  |
| `0x022D8EDC` | `u32` | clear colour on 1 |  |
| `0x022D8EF0` | `f32` | width / 2000 | `0x022D8EF4`  f32  height / 2000 |

The spin census is beside this page in [`graphics-thread-handshake-inert-spin-census.tsv`](graphics-thread-handshake-inert-spin-census.tsv): every
backward loop in 38,161 listed bodies whose body only tests registers, 19 in all. Seventeen are the
fence tests above. The other two wait for a latch that is loaded once outside the loop: `0x00560A60`
in `0x00560910` on `0x02CA8F94` and `0x00566163` in `0x00565E00` on `0x02CA96D4`. Each latch is set to 1 only
by an 11-byte callback (`0x00556560`, `0x00563550`), so each loop either falls through or never ends.

## State

| Address | What |
|---|---|
| `0x02EBA3F8` | the command-state word |
| `0x02EAF6D8` | the fence, never written |
| `0x02F8F2E0` | the staging pointer of `0x003A2D80` and `0x003A2E30` |
| `0x022CA5C8` | the pending end-of-frame callback |
| `0x022CFF10` | the TkSyncv handler table |
| `0x022D8EA0`, `0x022D8E50` | the current display record and the record array |

The options applier `0x002DDA30` rounds the words `+0x20` and `+0x22` of the in-game options record `[0x0215E6E0]` up
to even, writes them back and copies them beside the GS environment globals (`0x002DDB0B`-`0x002DDB44`). The seed
`0x0036D280` clears both copies with one 8-byte store.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x022D8EBC` | `i32` | 0 (zero-filled tail) | options `+0x20`, made even | `0x0036D280`, 0 (`0x0036D296`); `0x002DDA30` (`0x002DDB44`) | no instruction |
| `0x022D8EC0` | `i32` | 0 (zero-filled tail) | options `+0x22`, made even | `0x0036D280`, 0 (`0x0036D296`); `0x002DDA30` (`0x002DDB3C`) | no instruction |

Nothing else reads or writes the two copies: no other RIP-relative, image-base-relative or 32-bit offset reference
names them.

### The set-ups' own words

`0x0035E820` starts by storing -1 in `0x022CA62C` and zeroing the tick counters, then fills a semaphore descriptor at
`0x022CAE40` and makes two semaphores from it with `0x00863540`, which reads only the descriptor's maximum count `+0x04`
and initial count `+0x08` (`0x0086355E`, `0x00863565`): `[0x022CA610]` with a maximum of `0x10000` and `[0x022CA618]` with a
maximum of 1, both starting at 0. It then starts the pacer's worker `0x0035EA40` as a thread (`0x008636E0`, `0x00863610`),
spins until the worker reports itself running (`0x022CA630`, `0x0035E930`) and registers `0x0035EC90` as handler 0.

`0x00368DD0` starts the TkSyncv thread from a thread descriptor at `0x022CFEA0`. `0x008636E0` reads three of the
descriptor's words: the entry `+0x08` (`0x0086376B`), the stack size `+0x18` (`0x00863789`, passed to the thread's
creation) and the priority `+0x28` (`0x00863781`), which `0x00863430` turns into the thread priority `(32 - p) / 2`.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x022CA5F8` | `u32` | 0 (zero-filled tail of `.data`) | 1 once the set-up has run; while it is non-zero, `0x0035E760` and each pass of the worker `0x0035EA40` call `0x003691B0(0)` when handler 0 of the table `0x022CFF10` (the address `0x00369160` returns) is set | `0x0035E820`, 1 (`0x0035E84D`) | `0x0035E760` (`0x0035E764`); `0x0035EA40` (`0x0035EB0E`) |
| `0x022CA604` | `u32` | 0 (zero-filled tail of `.data`) | the pacer's mode, its second argument. While `0x022CA608` is 0, the handler `0x0035EC90` uses it once the sync count has reached its target (`0x0035ECCC`): mode 1 sets the pending flag `0x022CA600` only on a sync with bit 13 of `0x022CA60C` clear, mode 2 only with that bit set, any other value on every sync | `0x0035E820`, 0 (`0x0035E88A`); `0x0035EB70` (`0x0035EC28`) | `0x0035EC90` (`0x0035ECCC`) |
| `0x022CA628` | `u32` | 0 (zero-filled tail of `.data`) | the tick count the pacer was last given, `max(n, 1)` with a signed compare (`cmovg`, `0x0035EC1C`), the value it also stores at `0x022CA5F4`; 1 after the set-up | `0x0035E820`, 1 (`0x0035E85D`); `0x0035EB70` (`0x0035EC5F`) | no instruction names it |
| `0x022CA62C` | `i32` | 0 (zero-filled tail of `.data`) | the handle the set-up gets from `0x005C5230(2, 0x0035E760, -1)` (`0x0035E984`), -1 while none is held. A set-up that finds a handle held (not -1, `0x0035E948`) first passes it back through `0x005C5230` (`0x0035E956`, `0x0035E966`). `0x005C5230` is `xor eax, eax; ret`, so the word is 0 after every set-up | `0x0035E820`: -1 (`0x0035E828`, `0x0035E96B`); the result (`0x0035E98E`) | `0x0035E820` (`0x0035E948`, `0x0035E95B`) |
| `0x022CA634` | `u32` | 0 (zero-filled tail of `.data`) | the worker's run flag: the set-up sets it before it starts `0x0035EA40`, which loops while it is non-zero; the shutdown `0x0035E700` clears it, releases both semaphores and sleeps 1 ms at a time until the worker's running flag `0x022CA630` is 0 | `0x0035E820`, 1 (`0x0035E910`); `0x0035E700`, 0 (`0x0035E70B`) | `0x0035EA40` (`0x0035EA71`, `0x0035EAA0`, `0x0035EACD`, `0x0035EB30`) |
| `0x022CAE44` | `u32` | 0 (zero-filled tail of `.data`) | the semaphore descriptor's maximum count: `0x10000` for `[0x022CA610]`, then 1 for `[0x022CA618]`. The first store is 8 bytes and also writes 0 into the initial count `0x022CAE48` | `0x0035E820` (`0x0035E896`, 8 bytes; `0x0035E8BA`, 1) | `0x00863540` (`0x0086355E`), through the descriptor `0x0035E820` passes (`0x0035E8A7`, `0x0035E8C4`) |
| `0x022CAE54` | `u32` | 0 (zero-filled tail of `.data`) | descriptor `+0x14`, set to 0; `0x00863540` does not read it | `0x0035E820`, 0 (`0x0035E8A1`) | no instruction names it |
| `0x022CFEA8` | `void*` | 0 (zero-filled tail of `.data`) | the TkSyncv thread descriptor's entry, `0x00369100` | `0x00368DD0` (`0x00368E3B`) | `0x008636E0` (`0x0086376B`), through the descriptor `0x00368DD0` passes (`0x00368E97`) |
| `0x022CFEB0` | `void*` | 0 (zero-filled tail of `.data`) | `0x022CBEA0`, the `0x4000` bytes just below the descriptor; `0x008636E0` does not read it | `0x00368DD0` (`0x00368E52`) | no instruction names it |
| `0x022CFEB8` | `u32` | 0 (zero-filled tail of `.data`) | the stack size, `0x4000` | `0x00368DD0` (`0x00368E31`) | `0x008636E0` (`0x00863789`), through the descriptor |
| `0x022CFEC0` | `void*` | 0 (zero-filled tail of `.data`) | `0x02EAF6D0`, the address the vertical-sync set-up also puts in its own descriptor (`0x0035E8F5`); `0x008636E0` does not read it | `0x00368DD0` (`0x00368E72`) | no instruction names it |
| `0x022CFEC8` | `u32` | 0 (zero-filled tail of `.data`) | the priority, `0x1E`, which `0x00863430` sets as thread priority 1 | `0x00368DD0` (`0x00368E65`) | `0x008636E0` (`0x00863781`), through the descriptor |
| `0x022CFED4` | `u32` | 0 (zero-filled tail of `.data`) | descriptor `+0x34`, set to 0; `0x008636E0` does not read it | `0x00368DD0` (`0x00368E4C`) | no instruction names it |
| `0x022CFEE8` | `u32` | 0 (zero-filled tail of `.data`) | the low 32 bits of the address `0x008636E0` returns for the thread (the 8-byte holder of its thread object) | `0x00368DD0` (`0x00368EAE`) | no instruction names it |
| `0x022CFEFC` | `u32` | 0 (zero-filled tail of `.data`) | the maximum count `0x10000` of the semaphore descriptor `0x022CFEF8`, from which `0x00368DD0` makes both `[0x022CFEEC]` and `[0x022CFEF0]`. The store is 8 bytes and also writes 0 into the initial count `0x022CFF00` | `0x00368DD0` (`0x00368DE7`, 8 bytes) | `0x00863540` (`0x0086355E`), through the descriptor `0x00368DD0` passes (`0x00368E06`, `0x00368E18`) |
| `0x022CFF0C` | `u32` | 0 (zero-filled tail of `.data`) | descriptor `+0x14`, set to 0; `0x00863540` does not read it | `0x00368DD0` (`0x00368E00`) | no instruction names it |
| `0x022D7FB8` | `u8` | 0 (zero-filled tail of `.data`) | the TkSyncv thread's index `n`: `0x00368DD0` stores 0 and passes the byte's address as the thread's argument (`0x00368E84` to `0x008636E0`, `0x00368E9F` to `0x00863610`); the thread body `0x00369100` reads it and uses it for its semaphores and its handler | `0x00368DD0`, 0 (`0x00368E79`) | `0x00369100` (`0x0036910A`), through the argument |

## Modding notes

- Read this code from disassembly: the decompiler removes all eleven settle-spins.
- The publishers store `0x100` with a plain `mov`, so any bit a hook sets in the word is lost at
  the next publish.
- A hook that blocks inside a settle-spin burns the core; the waits are loops, not sleeps.
- Do not call `0x003A2D80` with fewer than 16 bytes.
- The batch's FRAME, SCISSOR, XYOFFSET, PRMODECONT, COLCLAMP and DTHE settings are not honoured by
  the GS replay ([PS2 VIF1 and VU1 emulation](../Engine-Core/ps2-vif1-vu1-emulation.md));
  the register list there is the one that reaches the PC renderer.

## Related

- [Render command list](render-command-list.md): the two GS command buffers and the object list.
- [Phyre frame](../PhyreEngine/the-frame.md): the draw that calls `0x0036D400` and its pass mask.
- [PS2 VIF1 and VU1 emulation](../Engine-Core/ps2-vif1-vu1-emulation.md): the GIF tag and the GS replay.
- [Frame update order](../Engine-Core/frame-update-order.md): the frame states and the end-of-frame group.
- [Legacy PS2 GS layer](legacy-ps2-gs-layer.md): the 512 × 448 surfaces the batch addresses.
