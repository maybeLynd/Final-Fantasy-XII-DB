[Home](../../README.md) / [Graphics](README.md) / Graphics thread handshake

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Graphics thread handshake: the shared command-state word, the GS register batch and the waits around them | system | Graphics | Render pipeline | How a frame hands its GS command stream over through the one dword at 0x02EBA3F8: the GS register batch 0x0036D400 writes, the three publishers that store a buffer address, a record count and 0x100 into the word, the reset burst at the start of every frame state, the settle-spin clear at the end, the vertical-sync callback that zeroes the word from the TkSyncv thread, the effect-capture bit, the fence word that nothing writes, and the list of the spin loops that cannot wait. | 0x02EBA3F8, 0x0036D400, 0x0036F360, 0x003A2D80, 0x003A2E30, 0x0036F2F0, 0x0036F2C0, 0x0036D7E0, 0x0022BFD0, 0x0035E9A0, 0x0035EC90, 0x00369100, 0x02EAF6D8, 0x003749F0, 0x00376050, 0x02F8F2E0, 0x00D10F88, 0x022D8EAC, 0x022D8EB4, 0x008636E0, 0x00863610, 0x00863520, 0x00863540, 0x00368C80, 0x00368C10, 0x00368DD0, 0x00369080, 0x00368F70, 0x022CFEF4, 0x022CFEE8, 0x022CFEEC, 0x022CFEF0, 0x022D7FB4 |

## What the player sees

Nothing directly. On the PlayStation 2 the game handed each frame's Graphics Synthesizer command
stream to the console's DMA hardware by writing a few registers, and waited for the hardware to
take it. The remaster keeps that code: every frame still builds the GS register batch, writes the
"kick" into one shared word in memory, spins until that word settles and clears its bits. The waits
finish at once unless the vertical-sync thread's end-of-frame callback writes the word between two
reads.

The thread layer behind the vertical-sync and background threads keeps the addresses of its thread holders and of
three of its semaphores in 32 bits. The game makes these allocations while it starts those threads, and while they
come back below the 2 GB line nothing goes wrong. A mod or loader that makes one of them land between 2 GB and 4 GB
makes the game crash at start-up; above 4 GB the address loses its high bits and the game reads the wrong memory.

## How it works

### The word

`0x02EBA3F8` is one dword, zero in the image. Every instruction that names it is a plain load or
store: 24 stores (18 `mov`, 4 `and`, 2 `or`) and 38 loads, with no `lock` prefix anywhere. The
values that pass through it are successive values of one cell, not separate fields:

| Value or operation | Written by | Meaning on the PS2 path |
|---|---|---|
| buffer address `& 0x3FF0`, then a record count | the three publishers | the start and length of a DMA chain |
| `0x100` (bit `0x100`) | the three publishers | the start bit, "batch published" |
| nine-store burst ending in 0 | the reset `0x0036F2F0` | the channel reset sequence |
| `and 0xFFFFFEF3` (bits `0x4`, `0x8`, `0x100` down) | the clear `0x0036F2C0` | batch accounted for |
| `or 0x10000`, then `and 0xFFFEFEFF` | effect capture | capture bit up, then bits `0x100` and `0x10000` down |
| 0 | `0x0036D7E0` | the vertical-sync callback's reset |

### The GS register batch

`0x0036D400(a, b)` builds the batch ([Phyre frame](../PhyreEngine/the-frame.md)
lists its callers and the pass bits that supply `a` and `b`). It reads the width `0x022D8EAC`
(512) and height `0x022D8EB4` (448), stores width / 2000.0 and height / 2000.0 at `0x022D8EF0` and
`0x022D8EF4` and 1.0 at `0x022D8EF8` and `0x022D8EFC`, and composes two register values:

- FRAME_1 at `0x022D8EC8`: frame index `[0x022D8EA8]` × pages per surface `[0x022D8EB8]`, with the
  buffer width `width >> 6` in the bits from `0x10000` and up¹;
- ZBUF_1 at `0x022D8ED0`: twice the pages per surface, with bit `0x1000000` set².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0036D477`-`0x0036D4B4` |
| ² | `0x0036D496`-`0x0036D4C2` |

</details>

It then writes into the current GS command buffer (`0x02EBEFC0` + 0x18 × `[0x02EBEFF0]`, see
[render command list](render-command-list.md)), one 16-byte record `{value, register}` per register:

| Step | What happens | Where in the code |
|---|---|---|
| 1 | a header record reserved first and filled at the end; |   |
| 2 | an A+D GIF tag (`0x003A2090`, register list `0xE`, end-of-packet bit); |   |
| 3 | FRAME_1 `0x4C`, ZBUF_1 `0x4E`, XYOFFSET_1 `0x18` (`(0x1000 − w) × 8`, `(0x1000 − h) × 8`), SCISSOR_1 `0x40` (0 to w−1, 0 to h−1), PRMODECONT `0x1A` = 1, COLCLAMP `0x46` = 1, DTHE `0x45` = 0; |   |
| 4 | when the table entry `0x00D10F88[(a != 0) \| (b != 0) << 1]` is non-zero: a screen clear (below); |   |
| 5 | TEST_1 `0x47` = `0x50000`, and `0x003A2020` writes the tag's loop count. | `0x0036D733` |

The table holds 0, `0x32001`, `0x31001` and `0x30000`; the chosen entry is the clear's TEST_1 value. The clear sets
TEST_1, PRIM (register 0) = 6, a sprite, and RGBAQ (register 1) to the colour `[0x022D8ED8]` when `[0x022D8EDC]` is
non-zero, else 0; `0x003A20C0` then emits XYZF2 (register 4) pairs that cover the screen in sprites 64 pixels wide.

With n the records after the header, `(cursor - header) / 16 - 1`¹, the header record
gets `n | 0x10000000` in its first qword² and `0x5000000011000000 | n << 32` in its
second³, or 0 there when n is 0⁴: a DMA
`cnt` tag followed by the VIF codes FLUSH (`0x11`) and DIRECT (`0x50`) with the record count. `0x0036D400` ends
with `0x003A1DB0` (`0x0036D7AD` or `0x0036D7C7`), which flips the buffers and calls the first publisher.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0036D75B`-`0x0036D77B` |
| ² | `0x0036D77E`-`0x0036D786` |
| ³ | `0x0036D78E`-`0x0036D7A4` |
| ⁴ | `0x0036D789`-`0x0036D78C`, `0x0036D7B9`-`0x0036D7BE` |

</details>

### The three publishers

`0x0036F360(buffer, records)` returns at once for 0 records. When the last record's first dword has
`0x30000000` under the mask `0x70000000` (a DMA `ref` tag) it writes the `cnt` record
`{0x10000000, 0}` after it, or over it when the buffer already holds `0x200` records¹. Then:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0036F372`-`0x0036F39C` |

</details>

| Step | What happens | Where in the code |
|---|---|---|
| 1 | it stores `buffer & 0x3FF0` and the record count into the word, the count one more when it wrote the `cnt` record after the last record; | `0x0036F3A6`<br>`0x0036F3AC`<br>`0x0036F38E`-`0x0036F391` |
| 2 | it loads the word three times and compares the values as cursors, looping until they fit; all three loads return the count it just stored, so the loop ends on its first pass; | `0x0036F3B2`-`0x0036F3E9` |
| 3 | it stores `0x100`. | `0x0036F3EB` |

`0x003A2D80(source, bytes)` rounds the size down to whole 16-byte records, copies the batch with
`memcpy`¹ to the staging buffer `[0x02F8F2E0]` (set to the GS buffer arena base
`[0x01FD4A78]` by the display-list set-up at `0x003A371A`), tests the fence (below), flips bit `0x400` of
the staging pointer (`xor 0x400`, `0x003A2DCB`), so two staging buffers alternate `0x400` bytes
apart, and stores the address, the count, and after its guard loop `0x100`². It is
called from `0x0044D80C`, `0x004537CE` and `0x00460F08`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00861EBA` |
| ² | `0x003A2E16` |

</details>

The address `0x003A2D80` stores is that of the buffer it has just filled, read before the flip, `& 0x3FF0`¹; the count is `bytes / 16`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003A2DB4`, `0x003A2DC5`, `0x003A2DD5` |
| ² | `0x003A2DDB` |

</details>

`0x003A2E30(source, bytes, pointer, bytes2)` does the same copy and appends two records by hand: a
`ref` record (`+3` = `0x30`, `u16` count `bytes2 / 16`, `+4` the pointer as a 32-bit image address
through `0x0020E620`) and a `cnt` record (`+3` = `0x10`, `+0xC` = `0x0404`, `+0xF` = 1), then
publishes count + 2¹ and, after its guard loop, `0x100`². Its only route is the guard
stub `0x0045BAD0` (`cmp byte [rcx], 0` / `jne 0x0045BAE0`), called from `0x002F4020` at `0x002F42C2`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003A2EFC` |
| ² | `0x003A2F59` |

</details>

The `ref` record's second qword is 0¹. The `cnt` record has the `u16` count 0, `+4` =
`0x0020E620(0)`, which is `0 - [0x01F83530]`, and 0 at `+8`². The stores into the word come
after the fence: the address of the buffer just filled, read before the `0x400` flip, `& 0x3FF0`, then count + 2³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003A2EA6` |
| ² | `0x003A2EB6`-`0x003A2ECF` |
| ³ | `0x003A2EDC`-`0x003A2F06` |

</details>

The guard loops of `0x003A2D80` and `0x003A2E30` first wait for a non-zero word¹. `0x003A2D80` stores `bytes / 16` as the count, so a call with fewer than 16
bytes stores 0 and that loop has nothing that ends it on the thread that runs it.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003A2DE1`-`0x003A2DE9`, `0x003A2F10`-`0x003A2F18` |

</details>

### The fence nothing writes

`0x02EAF6D8` is zero in the image and every one of its 17 references is a load, in nine functions.
Each is the hoisted form `mov eax, [0x02EAF6D8]; and eax, 0x100; test eax, eax; jne` back to the
`test`, which never reloads. With the word at 0 every one falls through: `0x0036F2F0`'s at
`0x0036F300`, the publishers' at `0x003A2DC1` and `0x003A2EE8`, and the rest in `0x0024D370`, `0x00259030`,
`0x002590F0`, `0x003749F0`, `0x00375500` and `0x00376050`.

### The reset burst

`0x0036F2F0` runs at the start of every frame state¹, again at `0x0022A87F` and `0x0022B2FD`, in the effect-capture
draw `0x003749F0` (`0x00374ACE` or `0x00374AD7`) and in `0x00376220`. After the fence it stores nine values with no branch between them²: the low dword of the address `0x022D9B50`, `0x7FFF0`, 0, the address twice,
`(word & ~4) | 8`, `word & ~0x30`, `0x14D`, and 0. No instruction in the image tests bits `0x4`, `0x8`, `0x10`,
`0x20` or the value `0x14D`; the burst ends with the word at 0.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0022A7E7`, `0x0022AF5E`, `0x0022B004`, `0x0022B6E4`, `0x0022B7E6`, `0x0022B8ED`, `0x0022BC35` |
| ² | `0x0036F30D`-`0x0036F352` |

</details>

### The settle-spin and the clear

`0x0036F2C0` is nine instructions: load the word into `ecx`, load it into `eax`, compare, loop back
while they differ¹, then `and dword [0x02EBA3F8], 0xFFFFFEF3`².
The loop repeats only when a store lands between the two loads. A decompiler folds the two loads
into one and shows only the `and`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0036F2D0`-`0x0036F2DE` |
| ² | `0x0036F2E0` |

</details>

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

The vertical-sync set-up `0x0035E820` registers `0x0035EC90` as handler 0 with `0x00369070`¹, and
the thread body `0x00369100` (created by `0x00368DD0` under the name `TkSyncvThread%d`) waits on its
semaphore `[0x022CFEEC + 4n]`², calls handler n of the table `0x022CFF10`³ and then,
unless `0x0017D3E0` reports the debug byte `+0xD07` of `[0x001D50D0()]` set, releases the next semaphore
`[0x022CFEF0 + 4n]`⁴, without end. A null handler is skipped⁵, and `0x0017D3E0`
answers 0 when `0x001D50D0()` is null⁶.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0035E93A` |
| ² | `0x00369128` |
| ³ | `0x0036913A` |
| ⁴ | `0x0036914D` |
| ⁵ | `0x00369135` |
| ⁶ | `0x0017D3EC` |

</details>

`0x0035EC90` counts vertical syncs in `0x022CA5F0`. When the count reaches `0x022CA5F4` and its mode
test passes it sets `0x022CA600`¹; while `0x022CA600` is set it calls the pending callback
and clears `0x022CA5C8`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0035ECFE` |
| ² | `0x0035ED12`-`0x0035ED20` |

</details>

The compare is signed¹; on a sync below the target the handler goes straight to the input
poll, so it neither sets the flag nor calls the callback. The mode is `0x022CA608` when that is non-zero, else
`0x022CA604`². With `0x022CA600` set and no callback stored, nothing is called and
`0x022CA5C8` stays 0³. The handler itself never resets the count or clears `0x022CA600`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0035ECBE`-`0x0035ECC0` |
| ² | `0x0035ECC2`-`0x0035ECD4` |
| ³ | `0x0035ED19` |

</details>

On every call `0x0035EC90` also increments the tick counter `0x022CA5E0`
(and `0x022CA5E8` while `0x022CA5FC` is 0), polls the input channels through `0x0035FCA0`¹, and ends by
tail-jumping to `0x003690F0`², which releases the semaphore `[0x022D7F90]`³ that
`0x00369170` waits on.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0035ED2B` |
| ² | `0x0035ED34` |
| ³ | `0x00863800` |

</details>

The callback `0x0022BFD0` runs
`0x00368A70` and then `0x0036D7E0`, which stores 0 in the word¹ and points `0x022D8EA0` at
the 0x28-byte display record `0x022D8E50 + 0x28 × [0x022D8EA8]`. This store comes from the TkSyncv
thread, so a settle-spin on the frame thread can see the word change between its two loads.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0036D7E7` |

</details>

### The thread and semaphore wrappers

The vertical-sync set-up and the Tk threads use a thin layer over the Windows calls:

- `0x008636E0(desc, name, arg)` makes a `crossThreadImpl` thread object of 0x28 bytes (`0x00863430`, the name
  "UnknownThread" when no name is given), files the name in the map `0x02EB37B8` under the thread's id
 ¹, and `0x00863610(thread, arg)` stores
  the argument and starts it (`ResumeThread`; `0x0035E92A`, `0x00368D53`);
- the object holds the vtable `0x01CCFA88`, the handle `+0x08`, the id `+0x10`, the entry `desc +0x08` at
  `+0x18` and the argument at `+0x20`². `0x00863430` creates the thread suspended
  (`CreateThread` with flags 4, `0x0086348B`), and `0x00863610` returns 0 whatever `ResumeThread` answers
 ³;
- `0x00863520(value, p)` calls `SetThreadPriority(value, (32 - p) / 2)` with its first argument unchanged
 ⁴; every caller but `0x00368EE7` passes a thread holder, not a handle (below);
- `0x00863540(desc)` makes a semaphore from the descriptor's counts (`0x008632E0`, `CreateSemaphoreW`; `0x0035E8A7`);
  `0x00863800` releases it by one, and `0x00863590` closes and frees it⁵;
- `0x00863690(sem, ms)` waits on a semaphore (`WaitForSingleObject`, `0x008636C6`), and `0x00863650(sem)` waits with no
  time-out (`WaitForSingleObject` with the handle `[[sem]]` and -1, `0x00863673`-`0x0086367C`); both return 0 for a
  null semaphore and 1 after the wait⁶;
- `0x008635F0(ms)` sleeps⁷.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x001AE550`, `0x001A5760` |
| ² | `0x00863726`-`0x00863776` |
| ³ | `0x00863646` |
| ⁴ | `0x00863532` |
| ⁵ | `0x0035E74B` |
| ⁶ | `0x00863666`-`0x00863682`, `0x008636AC`-`0x008636D1` |
| ⁷ | `0x0035E735`, `0x0035EAB3` |

</details>

`0x008636E0` returns the address of an 8-byte holder it takes from `0x00210EC0` (`malloc`, through `0x0085E730`;
`0x00863703`), which points at the thread object, and `0x00863540` returns the 8-byte semaphore object it takes the
same way¹. That object points at a second 8-byte block, which `0x008632E0` takes and in which it keeps
the handle²; when its own block cannot be had, `0x00863540` returns 0³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00863552` |
| ² | `0x00863301`-`0x00863326` |
| ³ | `0x00863572` |

</details>

The callers keep every thread holder and three of the semaphores as 32-bit values and widen
them again with `movsxd`:

| Address | Kept as | Widened at |
|---|---|---|
| every thread holder | the low dword in `eax` | `0x0035E925`, `0x00368D46`, `0x00368E9C` and `0x00369005`, each passed straight to the start `0x00863610`, which reads through it (`0x0086362D`) |
| the TkBGThread holder (`0x00368C80`) | dword `0x022CFEF4` (`0x00368D5F`) | `0x00368C4C`, on every pass of the thread body `0x00368C10`, for `0x00863520` (`0x00368C61`) |
| the TkSyncvThread holder (`0x00368DD0`) | dword `0x022CFEE8` (`0x00368EAE`) | never loaded: the store is the only reference to `0x022CFEE8` |
| the two TkSyncv semaphores | dwords `0x022CFEEC` and `0x022CFEF0` (`0x00368E12`, `0x00368E1D`) | `0x00369120` and `0x00369145` in the thread body `0x00369100`; `0x003691BA` (`0x003691B0`); `0x0036919A` (`0x00369190`) |
| the TkPowerOff semaphore (`0x00368FB5` in `0x00368F70`, made when bit `0x4` of `0x003692C0()` is set) | the low dword in `ebx` (`0x00368FC1`) | the thread argument of `0x008636E0` and `0x00863610` and the argument of `0x005C5230` (`0x00369010`), widened again by the thread body `0x00368AE0` (`0x00368AE4`) and the callback `0x00368AD0` |

The other four semaphores, made at `0x0035E8A7`, `0x0035E8C4`, `0x00368CC0` and `0x00368F15`, are kept whole in the qwords
`0x022CA610`, `0x022CA618`, `0x022D7F68` and `0x022D7F90`.

`0x00368C80` and `0x00369080` also read `0x022CFEF4 + 4 × [0x022D7FB4]`¹,
but only when `0x022D7FB4` is not 0². It is 0 in the image and every store writes 0³, so those four loads do not run.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00368D8F`, `0x00368DA4`, `0x003690BC`, `0x003690D1` |
| ² | `0x00368D6B`, `0x00369093` |
| ³ | `0x00368CAD`, `0x00368D65`, `0x00368D7B`, `0x0036908D`, `0x003690A8` |

</details>

An address comes back unchanged only while it is below `0x80000000`. From 2 GB to 4 GB the widened value has its top
32 bits set, and above 4 GB the high bits are lost. A holder from 2 GB to 4 GB faults at the first read through it,
at `0x0086362D`; one above 4 GB is read at the wrong address. The executable is large-address-aware with high-entropy
addressing (file characteristics `0x0022`, DLL characteristics `0x8120`), so the system may place the C-runtime
heap's blocks above 2 GB.

The holder is not the thread's handle. `CreateThread`'s handle is at `+0x08` of the object the holder points to¹, where `0x00863610` reads it for `ResumeThread`², and the creation sets the
priority with that handle³. `0x00863520` passes the holder itself⁴, so those calls name no thread handle; its result is discarded⁵. The one call
with a handle is `0x00368EE7`, with the pseudo-handle of `GetCurrentThread`⁶, which the dword round trip
at `0x00368ED9` keeps.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00863494` |
| ² | `0x0086362D`-`0x0086363B` |
| ³ | `0x008634A6` |
| ⁴ | `0x00368C61`, `0x00368D93`, `0x00368DA8`, `0x003690C0`, `0x003690DE` |
| ⁵ | `0x00863538` |
| ⁶ | `0x00368ED4` |

</details>

### Effect capture

The capture draws `0x003749F0` and `0x00376050` wait while bit `0x100` is set with a loop that reloads the
word¹, then `or` `0x10000` and immediately `and`
`0xFFFEFEFF` (`0x00374CEC`/`0x00374CF6`, `0x003761EC`/`0x003761F6`), so the capture bit is up for one
instruction and the `and` also drops bit `0x100`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00374C70`-`0x00374C7A`, `0x003761E0`-`0x003761EA` |

</details>

`0x00376050(record)` returns 1 without touching the word when the record's byte `+0x1D` differs from
`0x00358320()`¹. Otherwise, after `0x001E0580`, `0x002D7FA0` and `0x00182AD0`², the
record's byte `+0x1F` picks the wait: 2 uses the loop at `0x003761E0`, 3 the loop at `0x003761B0` and 4 the loop at
`0x00376170`, each after its fence test; any other value returns 0 with the word untouched³. The
transfer call before each loop is `0x0016D6A0`, which is `ret 0`, so it moves nothing. The three paths return 0.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0037609A` |
| ² | `0x003760A4`-`0x0037610B` |
| ³ | `0x00376139` |

</details>

No record takes those three paths. Of the 47 calls to `0x00375900`, only the one in `0x0024B7B0` files a kind `0x0C`
record¹, and it sets `+0x1F` to 1². So `0x00376050` returns 0 at `0x00376139`:
its loops at `0x00376170`, `0x003761B0` and `0x003761E0`-`0x003761EA` never run, and the `or` and `and` they share at
`0x003761EC`/`0x003761F6` never raise the capture bit ([Screen fades](screen-fades.md)).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0024B92A`, `0x0024B949` |
| ² | `0x0024B93C` |

</details>

### The Tk thread set-ups

`0x00368DD0` (above) also zeroes handler 0 of the table `0x022CFF10`¹ before it makes the two semaphores,
and builds the name with `0x0019C5D0(name, 0x18, "TkSyncvThread%d", 0)` (`__stdio_common_vsprintf_s`, import slot
`0x008C2E10` called at `0x0019C60F`; `0x00368E7F`).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00368DF9` |

</details>

`0x00368C80` starts the TkBG thread the same way from a descriptor at `0x022D7F20`: the entry `0x00368C10` at `+0x08`,
`0x022D3F20` at `+0x10`, the stack size `0x4000`, `0x02EAF6D0` at `+0x20`, the priority `0x24` and 0 at `+0x34`¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00368CD3`-`0x00368D1B` |

</details>

Before that `0x00368C80` makes the semaphore `[0x022D7F68]` from the descriptor `0x022D7F78` with a maximum
of `0x10000` and an initial count of 0, and zeroes the job slot `0x022D7F70`, `0x022D7F8C` and `0x022D7FB4`¹. The name is `TkBGThread%d` formatted with 0²; the index byte
`0x022D7FB9`, set to 0, is the thread's argument³. It keeps the holder's low dword at
`0x022CFEF4`⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00368C9B`-`0x00368CC5` |
| ² | `0x0019C5D0`, `0x00368D29` |
| ³ | `0x00368D22`-`0x00368D53` |
| ⁴ | `0x00368D5F` |

</details>

The thread body `0x00368C10(&n)` loops without end: it waits on `[0x022D7F68 + 8n]` with no time-out¹, calls the job `[0x022D7F70 + 8n]` when it is set², clears the job slot, and calls
`0x00863520` with the widened holder `[0x022CFEF4 + 4n]` and `0x24`³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00863650`, `0x00368C38` |
| ² | `0x00368C4A` |
| ³ | `0x00368C4C`-`0x00368C61` |

</details>

`0x00368F70` starts the TkPowerOff thread only when bit `0x4` of `0x003692C0()`, the dword `0x022D7FCC`, is set¹; otherwise it returns at once. It makes the semaphore from a stack descriptor with a maximum of 1
and an initial count of 0². Its stack thread descriptor holds the entry `0x00368AE0`,
`0x022CFF20` at `+0x10`, the stack size `0x4000`, `0x02EAF6D0` at `+0x20` and the priority 1³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00368F8E` |
| ² | `0x00368FAC`, `0x00368FB5` |
| ³ | `0x00368FC4`-`0x00368FEE` |

</details>

It starts the thread under the name `TkPowerOff` with the semaphore as its argument¹, and
stores what `0x005C5230(0x00368AD0, semaphore)` returns, 0, at `0x022CFF18`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00369000`, `0x0036900B` |
| ² | `0x00369027` |

</details>

## Layouts

<details>
<summary>Show the memory layouts</summary>

```
command-state word 0x02EBA3F8, as the PS2 code uses it
  publish   word = buffer & 0x3FF0 ; word = records ; word = 0x100
  clear     word &= 0xFFFFFEF3          bits 0x4, 0x8, 0x100
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
| `0x022D8EC8` | `u64` | FRAME_1 | value |
| `0x022D8ED0` | `u64` | ZBUF_1 | value |
| `0x022D8ED8` | `u32` |  | clear colour |
| `0x022D8EDC` | `u32` |  | clear colour on 1 |
| `0x022D8EF0` | `f32` |  | width / 2000 |
| `0x022D8EF4` | `f32` |  | height / 2000 |

The list of spin loops is beside this page in
[`graphics-thread-handshake-inert-spin-census.tsv`](graphics-thread-handshake-inert-spin-census.tsv): every
backward loop in 38,161 listed bodies whose body only tests registers, 19 in all. Seventeen are the
fence tests above. The other two wait for a latch that is loaded once outside the loop: `0x00560A60`
in `0x00560910` on `0x02CA8F94` and `0x00566163` in `0x00565E00` on `0x02CA96D4`. Each latch is set to 1 only
by an 11-byte callback¹, so each loop either falls through or never ends.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00556560`, `0x00563550` |

</details>

### Columns of graphics-thread-handshake-inert-spin-census.tsv

One row per inert loop, 19 rows.

| Column | Holds |
|---|---|
| `jump` | the address of the backward conditional jump that closes the loop; `target` is where it jumps back to, and `body` the loop's instructions from `target` to the jump, every one a `test`, `cmp`, `nop` or `pause` on registers or constants |

</details>

## State

<details>
<summary>Show the state it keeps</summary>

| Address | What |
|---|---|
| `0x02EBA3F8` | the command-state word |
| `0x02EAF6D8` | the fence, never written |
| `0x02F8F2E0` | the staging pointer of `0x003A2D80` and `0x003A2E30` |
| `0x022CA5C8` | the pending end-of-frame callback |
| `0x022CFF10` | the TkSyncv handler table |
| `0x022D8EA0`, `0x022D8E50` | the current display record and the record array |

The options applier `0x002DDA30` rounds the words `+0x20` and `+0x22` of the in-game options record `[0x0215E6E0]` up
to even, writes them back and copies them beside the GS environment globals¹. The seed
`0x0036D280` clears both copies with one 8-byte store.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002DDB0B`-`0x002DDB44` |

</details>

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x022D8EBC` | `i32` | 0 (zero-filled tail) | options `+0x20`, made even | `0x0036D280`, 0 (`0x0036D296`); `0x002DDA30` (`0x002DDB44`) | no instruction |
| `0x022D8EC0` | `i32` | 0 (zero-filled tail) | options `+0x22`, made even | `0x0036D280`, 0 (`0x0036D296`); `0x002DDA30` (`0x002DDB3C`) | no instruction |

Nothing else reads or writes the two copies: no other RIP-relative, image-base-relative or 32-bit offset reference
names them.

### The set-ups' own words

`0x0035E820` starts by storing -1 in `0x022CA62C` and zeroing the tick counters, then fills a semaphore descriptor at
`0x022CAE40` and makes two semaphores from it with `0x00863540`, which reads only the descriptor's maximum count `+0x04`
and initial count `+0x08`¹: `[0x022CA610]` with a maximum of `0x10000` and `[0x022CA618]` with a
maximum of 1, both starting at 0. It then starts the pacer's worker `0x0035EA40` as a thread²,
spins until the worker reports itself running³ and registers `0x0035EC90` as handler 0.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0086355E`, `0x00863565` |
| ² | `0x008636E0`, `0x00863610` |
| ³ | `0x022CA630`, `0x0035E930` |

</details>

Each pass of the worker `0x0035EA40` first calls `0x0017D3E0` and, while it answers 0, sleeps 1 ms with
`0x008635F0(1)` and asks again, leaving when the run flag `0x022CA634` is 0¹. It
then calls `0x00863650` with the semaphore `[0x022CA610]`, leaves when the run flag is 0, and reads the clock
`0x005A0820` as a double². The pass's value is the double at `0x022CA640` + 8 x
index³; the index starts at 0 and goes up by one a pass as a byte, so 255 is followed by 0⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0035EA92`-`0x0035EABF` |
| ² | `0x0035EAC1`-`0x0035EAD7` |
| ³ | `0x0035EADC` |
| ⁴ | `0x0035EA4F`, `0x0035EB2A`-`0x0035EB2D` |

</details>

A value below 0.0 makes the clock reading the new base and calls `0x00863690` with the semaphore
`[0x022CA618]` and `trunc(-value)`¹. Any other
value v calls it with `trunc(v - (clock - base))` only when `v - (clock - base)` is above 0.0². The base is 0.0 until a value below 0.0 has been seen³.
Then comes the call given below, and the loop goes on while the run flag is not 0⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0035EAE1`-`0x0035EAEE`, `0x0035EAFE`-`0x0035EB09` |
| ² | `0x0035EAF0`-`0x0035EB09` |
| ³ | `0x0035EA6E`-`0x0035EA77` |
| ⁴ | `0x0035EB0E`-`0x0035EB38` |

</details>

Before its first pass the worker calls the empty stub `0x0016D6A0`, stores 1 in the dword `0x022CA630`
and leaves at once when the run flag is 0¹; on every way out it stores 0 in
`0x022CA630`². The call that ends a pass is `0x003691B0(0)`, made only when the dword
`0x022CA5F8` is not 0 and the qword that the answer of `0x00369160()` points at is not 0³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0035EA5C`-`0x0035EA7C` |
| ² | `0x0035EB53` |
| ³ | `0x0035EB0E`-`0x0035EB25` |

</details>

`0x00368DD0` starts the TkSyncv thread from a thread descriptor at `0x022CFEA0`. `0x008636E0` reads three of the
descriptor's words: the entry `+0x08`¹, the stack size `+0x18` (`0x00863789`, passed to the thread's
creation) and the priority `+0x28`², which `0x00863430` turns into the thread priority `(32 - p) / 2`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0086376B` |
| ² | `0x00863781` |

</details>

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x022CA5F8` | `u32` | 0 (zero-filled tail of `.data`) | 1 once the set-up has run; while it is non-zero, `0x0035E760` and each pass of the worker `0x0035EA40` call `0x003691B0(0)` when handler 0 of the table `0x022CFF10` (the address `0x00369160` returns) is set | `0x0035E820`, 1 (`0x0035E84D`) | `0x0035E760` (`0x0035E764`); `0x0035EA40` (`0x0035EB0E`) |
| `0x022CA604` | `u32` | 0 (zero-filled tail of `.data`) | the pacer's mode, its second argument. While `0x022CA608` is 0, the handler `0x0035EC90` uses it once the sync count has reached its target (`0x0035ECCC`): mode 1 sets the pending flag `0x022CA600` only on a sync with bit `0x2000` of `0x022CA60C` clear, mode 2 only with that bit set, any other value on every sync | `0x0035E820`, 0 (`0x0035E88A`); `0x0035EB70` (`0x0035EC28`) | `0x0035EC90` (`0x0035ECCC`) |
| `0x022CA628` | `u32` | 0 (zero-filled tail of `.data`) | the tick count the pacer was last given, `max(n, 1)` with a signed compare (`cmovg`, `0x0035EC1C`), the value it also stores at `0x022CA5F4`; 1 after the set-up | `0x0035E820`, 1 (`0x0035E85D`); `0x0035EB70` (`0x0035EC5F`) | no instruction names it |
| `0x022CA62C` | `i32` | 0 (zero-filled tail of `.data`) | the handle the set-up gets from `0x005C5230(2, 0x0035E760, -1)` (`0x0035E984`), -1 while no handle is held. A set-up that finds a handle held (not -1, `0x0035E948`) first passes it back through `0x005C5230` (`0x0035E956`, `0x0035E966`). `0x005C5230` is `xor eax, eax; ret`, so the word is 0 after every set-up | `0x0035E820`: -1 (`0x0035E828`, `0x0035E96B`); the result (`0x0035E98E`) | `0x0035E820` (`0x0035E948`, `0x0035E95B`) |
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

</details>

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

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 2 calls with 2 other topics</summary>

**Platform** (explained on [phyre application](../PhyreEngine/phyre-application.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0035E700`](graphics-thread-handshake.md) | is called by | [`0x007A4310`](../PhyreEngine/phyre-application.md) (on phyre application) |

**Scripts and script commands** (explained on [graphics settings](../Engine-Core/graphics-settings.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00358320`](graphics-thread-handshake.md) | is called by | [`0x0034C7E0`](../Engine-Core/graphics-settings.md) (on graphics settings) |

</details>
