---
title: "File requests and the read queue: the request slots, how a load is queued, sized, read in parts and completed, and how a caller waits, asks or cancels"
kind: "system"
category: "Game files and data tables"
addresses: "0x0032E450, 0x022C31C0, 0x022C51C0, 0x022C51C8, 0x022C51D0, 0x01EED498, 0x0032EA90, 0x022C51F0, 0x0032E400, 0x002DF960, 0x0032E620, 0x003EB0D0, 0x0032E870, 0x0032E990, 0x0032EC40, 0x0032E780, 0x0032E7C0, 0x0032E070, 0x0032E040, 0x0032E520, 0x0032E4D0, 0x0032E590, 0x0032E2F0, 0x0032E330, 0x0032E370, 0x0032E3B0, 0x0046E030, 0x002DF780, 0x002DF6C0, 0x0046DFE0, 0x0046E0E0, 0x0215EFF4, 0x0035E810, 0x022CA5E0, 0x0035EA30, 0x003EADD0, 0x02B5E0E0, 0x0046DD50, 0x003E9780, 0x003BB790, 0x0050DFE0, 0x00249180, 0x022C5AF0, 0x022C59F0, 0x0032EA50, 0x0032ECE0, 0x0032ED20, 0x0051ED10, 0x0051EDB0, 0x002DF7B0, 0x0024AC30, 0x00365810, 0x002EF300, 0x00324510, 0x003DC5B0, 0x003EB100"
---

## What the player sees

Every file the game loads during play, from a map's script set to a menu image, is a request in this
queue. When more than 64 loads are outstanding, the code asking for the next one stops and services
the queue until a slot frees up, which can lengthen a load.

## How it works

### The slots

`0x0032E450` builds 64 slots of `0x80` bytes at `0x022C31C0` at boot: each gets its index at `+0x58`,
id `+0x64` = −1, state word `+0x20` = 0 and `+0x28` = 0, and the slots are chained through `+0x10`
(next) and `+0x18` (previous) into the free list headed at `0x022C51D0`. The pending list's head and
tail (`0x022C51C0`, `0x022C51C8`) start empty and the request counter `0x01EED498` starts at 1.
`0x0032EA90` calls it, resets the BGM stream reader (`0x003EB050`) and zero-clears the 256 per-kind size
override pointers at `0x022C51F0`.

`0x0032E990(atTail)` takes the free head and links it into the pending list, at the tail when
`atTail` is non-zero and at the head otherwise. `0x0032EC40(slot)` unlinks a slot from the pending
list, pushes it on the free list and sets its id to −1. Neither clears the rest of the slot.

### Sizes

`0x0032E400(kind, index)` returns −1 for kind `0xFF`. When the override pointer for the kind is non-null
and the index is below `0x400`, it returns that table's dword as it is. Otherwise it asks `0x002DF960`
and rounds a positive result up to a multiple of 64. The override table's only static writer is
`0x0032EA90`'s zero-clear (its readers are `0x0032E400` and `0x0032EB40`), so every shipped size comes from
`0x002DF960`. A caller passes the size it gets as the request's byte count.

### Making a request

`0x0032E620(kind, index, dest, bytes, descriptor)` stores the kind and index in `0x022C51D8` /
`0x022C51DC` and returns −1 for a negative index.

- When the BGM stream reader is not armed (`0x003EB0D0`: byte `+0x31` of `0x02B5E0E0`), it calls
  `0x0032E870(kind, index, dest, bytes, descriptor, 1)` for the whole file.
- When it is armed, it copies the descriptor with `0x80000` in its second dword and, on a non-zero id,
  makes the request chunked: `+0x22` = 1, part cap `+0x30` = `0x80000`, remaining `+0x34` = bytes,
  first part `+0x28` = `min(bytes, 0x80000)`, `+0x50` = 0, `+0x00` = 0, and the offset `+0x2C`
  truncated again to a multiple of `0x800`.

`0x0032E780(kind, index, …)` refuses a negative index and otherwise calls `0x0032E870` directly; its
only caller is the BGM stream reader `0x003EADE0`. `0x0032E7C0(path, dest, bytes, descriptor)` copies the
path into arena 8 (`0x0036A190`) and requests it as kind `0xFF` with the low 32 bits of the copy's
address as the index.

`0x0032E870` first stalls while the free list is empty, calling the pump `0x0032E070(0)`, `0x0046DFE0` and
`0x0035EA30` in a loop. It then takes a slot at the tail of the pending list and fills it:

- `+0x24` index, `+0x21` kind, `+0x28` bytes, `+0x20` state 1;
- `+0x2C` the descriptor's first dword (the file offset) truncated toward zero to a multiple of
  `0x800` (`cdq`, `and edx, 0x7FF`, `add`, `and 0xFFFFF800`: a non-negative offset is floored);
- `+0x38` and `+0x70` the destination, `+0x40` and `+0x48` the descriptor's `+0x10` and `+0x18`,
  `+0x60` its `+0x08`, `+0x50` = 0, and `+0x00`, `+0x22` and `+0x5C` zeroed;
- the id `+0x64` = counter × 64 + slot index; the counter then advances and wraps from `0xFFFFFF`
  back to 1.

It returns the id. A null descriptor gives offset 0 and no callbacks.

`0x0051ED10(kind, index, callback)` loads a whole file into arena 5: it sizes it (`0x0032E400`), takes
the block top-down (`0x0036A190`) under that arena (`0x0036C1D0(5)`, `0x0036C140`) and files it with a
descriptor whose callback word is the low 32 bits of `callback` and whose delivery and failure
callback is `0x0051EDB0`. That stub sign-extends the word (`movsxd rax, ecx`) and jumps to it, so the
caller's function runs with the destination and the flag the pump passes; it returns the
block.

### The pump

`0x0032E040` calls the pump `0x0032E070(0)` when `0x001EDE80()` or `0x001D6B70()` is non-zero. Its callers
are the main loop's mode bodies (`0x0022A770`, `0x0022AF50`, `0x0022B000`, `0x0022B6E0`, `0x0022B7E0`,
`0x0022B8C0`, `0x0022BC20`), boot `0x0022A0B0`, the script native `0x0036EEB0` and `0x00379E30`. The pump is
also run by the stall in `0x0032E870` and by the drain `0x0032E520(0)`.

The pump works on the pending head and keeps going while the head changes; a state that has to wait
ends the pass:

| State | Meaning | What the pass does |
|---|---|---|
| 1 | queued | if the BGM stream reader takes this pass (`0x003EADD0` returns 1), end the pass. A zero byte count: delivery callback, state 0, release. Kind `0xFF`: `0x002DF6C0(path, dest, bytes, offset)`, which always returns 0, then `+0x08` = `0x0035E810()` and state 2. Any other kind: `0x0046E030(kind, index, offset, bytes, dest)` → `0x002DF780`, then `+0x08` = `0x0035E810()` and state 2 |
| 2 | issued | `+0x00` += `0x0035E810()`, `+0x08` = the same value, state 3 |
| 3 | waiting | while the read status `0x0215EFF4` is −1 (`0x0046DFE0` returns 2), end the pass; otherwise state 5 when the status is 0 or more (`0x0046E0E0`), 6 when negative, and continue with that state |
| 4 | cancelled | while the read is in flight, end the pass; then the cancel callback with `+0x28` = 0 when one is set, state 0, release |
| 5 | delivered | not chunked: delivery callback and release. Chunked: remaining `+0x34` −= the part; when something is left, the offset `+0x2C` and destination `+0x38` advance by the part and the part callback decides; when nothing is left, delivery callback and release |
| 6 | failed | not chunked: failure callback and release. Chunked: failure callback and release |

In a chunked request a part-callback result of 1 sizes the next part as `min(+0x30, +0x34)`, zeroes
`+0x00`, truncates the offset to `0x800` again and requeues it in state 1; any other result is stored
at `+0x23` and ends the pass, and a stored 2 makes the next pass ask again. `0x0032E3B0` returns 1 when
no part callback is set, and the part callback slot `+0x50` is only ever written as 0 (`0x0032E6FF`,
`0x0032E959`), so in the shipped game every chunked request runs part after part.

`0x0035E810` returns the 64-bit tick counter `0x022CA5E0`, which only `0x0035EC90` increments (the callback
`0x0035E820` registers). Slot `+0x00` therefore sums counter readings; nothing reads it.

After the queue, every pass ends the same way: `0x0046DD50` (the read layer's tick), `0x003E9780`, and
`0x003BB790` when `0x0036FD50()` is non-zero. When the pending list is empty the pass also steps the
BGM stream reader (`0x003EADD0`) first.

### Callbacks

- **Delivery** `0x0032E330(slot)`: `+0x40(+0x60, +0x70, 1)` when set; for kind `0xFF`, frees the path
  (`0x003697F0`).
- **Failure** `0x0032E370(slot)`: `+0x40(+0x60, +0x70, 0)` only when the byte count `+0x28` is −1; then
  frees a kind-`0xFF` path. A failed read with any other byte count calls nothing, and a −1-size request
  reaches this only when the previous read had failed.
- **Cancel** `0x0032E2F0(slot)`: `+0x48(+0x60)` with `+0x28` = 0 when set, then state 0.

The first argument is the descriptor's `+0x08` word, not the buffer; a requester reads its bytes at
the destination.

### A refused request

The read issuer `0x002DF780` tests the size table, not the request: it compares the table entry
`[0x02EC3EE0 + 4 × (5000 × kind + index)]` with −1 (`0x002DF7B0`) and returns without reading on −1. `0x0032E870` stores the
caller's byte count as it is (`0x0032E92C`). So a request whose table entry is −1 completes with the previous read's
status, normally as delivered, with nothing written, whatever byte count the caller passed.

`0x0032E400` hands the −1 back to the caller (`0x0032E43B`-`0x0032E448` round only a positive value). The table is read
whole at start-up (`0x002E0432`-`0x002E0444`) and never written after.

Every requester is in [`file-requests-and-the-read-queue-requesters.tsv`](file-requests-and-the-read-queue-requesters.tsv): the
51 call sites of `0x0032E620`, the three of `0x0051ED10` and the two of `0x0032E780`, with where each takes its kind,
index and size, whether it tests the size before filing, and what follows when the buffer is never written.

- 39 of the 51 sites size the file through `0x0032E400`: 24 skip a size of 0 or less, 4 skip only a negative size,
  and 11 file it without a test (the table's guard column names what each tests instead); 3 others test the size
  in the record builder that stores it (`0x003DD4C0`, `0x003DF440`, `0x003E9F80`).
- The area loader `0x0032FCA0` tests the entry's sign before its four fixed-size requests.
- `0x0032EB40` requests a file only when its size is above `0x800` bytes.
- The model binding's `0x002EAD50` is reached only through `0x002E6700`'s positive-size test (`0x002E6789`).
- Six fixed requests file without a test but name entries every table sizes: `0x00291C80`, `0x002C8EE0`, `0x003658F0`,
  `0x0039C3F0`, `0x003B53C0`, `0x002FC860`. `debug_fileread` (`0x0050DFE0`) passes the script's values.

The requests that do meet a −1 in a shipped table:

| Requester | Entries | Tables | What follows |
|---|---|---|---|
| `0x0024AC30` | kind 35, `n + 7` | every table | the callback `0x0024ACF0` stores 1 at `0x02091094`, so the overlay counts as loaded with `[0x01FD4A18]` as it was |
| `0x00365810` | kind 7, indices 218-223 (`0x00D10C98`) | KR, CN | the callback `0x00364380` sets the slot's loaded bit in `[0x022CBE00] + 0x240` over a zero-length block (`0x0036BC60` clamps a negative size to 0) |
| `0x002EF300` | kind 1, indices 117-132 (`0x75` + slot) | JP, CH, ASIA, IN | no callback; the caller `0x0050D9A0` pumps the queue (`0x0032E520(0)`) and goes on with the save buffer `0x02164280` as it was |
| `0x0051ED10` from `0x003EAC40` | kind 9, index `0x1F` | UK | the caller's callback, through `0x0051EDB0`, runs on a zero-length block nothing wrote |
| `0x00324510` | kind 26, its own list of 301 at `0x022C27B8` | every table sizes only 166 kind-26 entries | `0x003244F0` counts the request done with its part of `[0x022C27B0]` unwritten |
| `0x003DC5B0` | the caller's | any | `0x003DC8D0` returns the −1 size and a flag `0x003DC5B0` never tests; the callback `0x003DC340` binds the block unwritten |

The BGM stream reader (`0x0032E780`'s two sites) never files in story play. Only `0x003EB100` arms the record
`0x02B5E0E0` (`0x003EB139`), and its one caller is the verb `bgmstreamread` (`0x448`, `0x00354690`), which only the developer
menu `bin/ctrl` calls ([music](../Sound-And-Music/music-table.md)). The reset `0x003EB050` leaves `+0x31` at 0, so `0x003EADE0` returns at once
(`0x003EADF4`-`0x003EADF8`). Armed, it would file kind `0x24` parts, which every table leaves at −1, and hand the unwritten
buffer to the sound library (`0x002DF660`), whose `0x0021D770` refuses a byte count of 0 or less (`0x0021D7AD`-`0x0021D7AF`).

In every one of the twelve tables kinds 3, 6, 17, 18, 27, 29, 31, 35, 36 and 40 are −1 throughout, and no entry is 0.
The UK table leaves kinds 5 and 8 at −1 throughout, so it sizes no zone script.

### Waiting, asking and cancelling

- `0x0032E520(0)` drains: it pumps, and while the pending list is non-empty or a read is in flight it
  waits (`0x0035EA30`) and pumps again. `0x0032E520` with a non-zero argument only answers 1 when the
  pending list is non-empty or a read is in flight, without pumping.
- `0x0032E4D0(id)` answers 1 when the slot `id & 0x3F` still carries that id and a non-zero state; 0 and
  −1 are refused.
- `0x0032E590(id)` cancels a request whose slot still carries the id: it clears the delivery callback
  `+0x40` and frees a kind-`0xFF` path at once; a request in states 2 or 3 goes to state 4 for the
  pump to finish; state 4 is left alone; any other state runs the cancel callback and is released at
  once. Its callers are `0x002FC3C0`, `0x003B1310`, `0x003B1710` and `0x003B18E0`.
- `0x00379E30(h)`, run by the slot handlers `0x003DEC90` (`0x003DED09`, its state 2) and `0x003DEE10` (`0x003DEEB9`), pumps
  (`0x0032E040`, then `0x0035EA30(0)`) while `0x00379E60(h)` holds. For `h` other than 0 that is: the dword `+0x28` of
  record `h & 0xF` of the sixteen `0x70`-byte records at `0x02ADD170` still equals `h`; for 0, the qword `0x02ADD870`
  is non-zero. `0x00379D60` clears the records, numbers each `+0x28` as `0x10 + i`, and clears `0x02ADD870`.

`0x0035EA30(n)` is `0x0035EB70(n, 0)`: off the thread `0x00368C70` names it spins until the tick counter
has advanced by `max(n, 1)`; on that thread it only updates the frame bookkeeping and does not wait.

### The BGM stream reader

`0x003EADD0` steps the BGM stream reader, whose state lives at `0x02B5E0E0` (`+0x31` active, `+0x30` state 1-8), which
files its own requests through `0x0032E780`. It returns 1 only in states 1 and 7, on the call where it
submits, and 0 when inactive, while waiting (states 2 and 8 test its request with `0x0032E4D0`, state 4
tests `0x002DEE90`) and when it finishes. The pump's state 1 gives up the pass when it returns 1, so the
reader's request goes first.

Only `0x003EB100` arms the reader (kind `0x24`, index = its argument, `+0x30` = 1, `+0x31` = 1, and only
when its buffer `+0x08` exists); its only caller is `bgmstreamread` (`0x0448`, `0x00354690`). `0x003EB010`
releases it (`0x003EAD10`, then frees `+0x08`; callers `usebgmstream` `0x003557C0` and `0x002628B0`),
`0x003EB050` resets it at init (from `0x0032EA90`), and `0x003EB0D0` is the query (callers `0x0032E620`,
`bgmstreamplaysync` `0x003550F0` and `getbgmstreamstatus` `0x00355FB0`).

Of the 10,036 decompiled
scripts, only the two ATEL control scripts `ps2data_image_ff12_ch_bin_ctrl` and
`ps2data_image_ff12_in_bin_ctrl` use the BGM stream verbs, so in normal play the reader is never
armed, no request is chunked, and `0x003EADD0` never takes a pass. Kind `0x24` is also one of the
unsized kinds of the size table.

### The read-source switches

Two 256-byte bit tables, one bit per resource kind, survive from the PS2 build: `0x022C5AF0` (read from
the hard disk) and `0x022C59F0` (read from the PC). Boot (`0x0022A0B0` → `0x003694D0`) clears both
(`0x0032EAF0(0)`, `0x0032EB10(0)`); `0x0032EB10` then sets kind `0xFF`'s bit in the PC table.

| Verb | Native | Body |
|---|---|---|
| `getreadfromhdd` `0x037A` | `0x00342DD0` | `0x0032EA50(kind)`: the kind's bit in `0x022C5AF0` |
| `setreadfromhdd` `0x0379` | `0x00342960` | `0x0032ECE0(kind, flag)`: sets or clears the kind's bit in `0x022C5AF0` |
| `setreadfrompc` `0x0377` | `0x003420B0` | `0x0032ED20(kind, flag)`: the same in `0x022C59F0`; kind `0xFF` is always set |

Nothing else reads either table: the builder, the pump and the read issuer route every request the same
way whatever the bits say.

### Which kinds are requested

`0x0032E620` has 51 call sites in 38 functions. 38 pass a fixed kind: an immediate, a constant folded
through a register, one of a closed set (`0x002FC96F`: `0xB` or `0x26`; `0x0032FCA0`: 5, 8, 1 or `0x25`),
or a kind from `0x002ED6F0`'s class table, none of them `0xFF`. Nine pass a caller's parameter and three
a signed word of a record (a word of −1 sign-extends to −1, which the builder refuses first).
`debug_fileread` (`0x2007`, `0x0050DFE0`) passes a kind popped from the script.

## Layouts

Slot (`0x80`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u64` |  | counter sum |
| `+0x08` | `u64` |  | counter at issue |
| `+0x10` | `...` | next |  |
| `+0x18` | `...` | prev |  |
| `+0x20` | `u8` | state |  |
| `+0x21` | `u8` | kind |  |
| `+0x22` | `u8` | chunked |  |
| `+0x23` | `u8` |  | part result |
| `+0x24` | `i32` | index | or path |
| `+0x28` | `i32` | bytes | current part |
| `+0x2C` | `i32` |  | file offset |
| `+0x30` | `i32` |  | part cap |
| `+0x34` | `i32` | remaining |  |
| `+0x38` | `...` | destination | current part |
| `+0x40` | `...` |  | delivery/failure callback |
| `+0x48` | `...` |  | cancel callback |
| `+0x50` | `...` |  | part callback |
| `+0x58` | `u32` |  | slot index |
| `+0x5C` | `u32` | requesterZeroed5C |  |
| `+0x60` | `u32` |  | callback word |
| `+0x64` | `u32` | id |  |
| `+0x70` | `...` | destination | start |

Descriptor:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i32` |  | file offset |
| `+0x08` | `u32` |  | callback word |
| `+0x10` | `...` |  | delivery/failure callback |
| `+0x18` | `...` |  | cancel callback |

Queue:

| Address | Type | Name | Meaning |
|---|---|---|---|
| `0x022C51C0` | `...` |  | pending head |
| `0x022C51C8` | `...` |  | pending tail |
| `0x022C51D0` | `...` |  | free head |
| `0x022C51D8` | `...` | kind |  |
| `0x022C51DC` | `...` | index |  |
| `0x022C51F0` | `void*[256]` | size overrides | 256 size override pointers |
| `0x01EED498` | `...` |  | request counter |

| Address | Type | Name | Meaning |
|---|---|---|---|
| `0x0215EFF4` | `...` | read status | -1 in flight, >= 0 delivered, other negative failed |

The fields are listed access by access in
[`file-requests-and-the-read-queue-slot-accesses.tsv`](file-requests-and-the-read-queue-slot-accesses.tsv),
[`file-requests-and-the-read-queue-read-status-accesses.tsv`](file-requests-and-the-read-queue-read-status-accesses.tsv) and
[`file-requests-and-the-read-queue-size-override-accesses.tsv`](file-requests-and-the-read-queue-size-override-accesses.tsv).

## Shipped data

[`file-requests-and-the-read-queue-constant-requests.tsv`](file-requests-and-the-read-queue-constant-requests.tsv)
lists 238 call sites of the request and size entries (`0x0032E620` 65, `0x0032E400` 86, `0x00249210` 52,
`0x002493D0` 21, `0x00249180` 11, `0x0032E3F0` 2, `0x00249350` 1) with the kind, id and file name where they
are constant. 203 sites carry a constant kind: 121 of kind 7, 34 of kind 9, 18 path requests
(`0xFF`), 8 of kind 5 and 22 over eleven other kinds. No decompiled script in any locale calls
`debug_fileread`.

## Operations

Per request: one slot, one read (or one per 512 KB part while the BGM stream reader is armed) and one
callback.
Per pump pass: as many state steps as the pending head allows before a wait.

## State

The 64 slots and the three list heads, the request counter, the read status word `0x0215EFF4`, the tick
counter `0x022CA5E0` and the BGM stream reader at `0x02B5E0E0`.

`0x00324510`, the `.nmb` builder, never starts: nothing stores the state that begins its build ([authored data tables](authored-data-tables.md)), so its descriptor and cursor below stay 0 in shipped play.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x022C31D8` | `void*` | 0 (zero-filled tail of `.data`) | slot 0 `+0x18`, its previous link. `0x0032E450` chains the 64 slots with a cursor that starts here (`0x0032E460`); the loop's first pass stores the address `0x80` below slot 0, and after the loop it stores 0, so the first slot of the free list has no previous slot | `0x0032E450` (`0x0032E47A`, the first pass; `0x0032E4AA`, 0) | the slot field `+0x18` accesses of [file-requests-and-the-read-queue-slot-accesses.tsv](file-requests-and-the-read-queue-slot-accesses.tsv), through a slot pointer |
| `0x022C5150` | `void*` | 0 (zero-filled tail of `.data`) | slot 63 `+0x10`, its next link: the loop's last pass stores `0x022C51C0`, the address just past the last slot, and the builder then stores 0 | `0x0032E450` (`0x0032E48A`, the last pass; `0x0032E4B8`, 0) | the slot field `+0x10` accesses of the same table, through a slot pointer |
| `0x022C5A0F` | `u8` | 0 (zero-filled tail of `.data`) | byte `0x1F` of the read-from-PC table `0x022C59F0`, the bits of kinds `0xF8` to `0xFF` (the byte index is the kind divided by 8, signed, `0x0032ED23`-`0x0032ED36`); bit `0x80` is kind `0xFF`, which both writers keep set | `0x0032EB10` (`0x0032EB28`, the 256-byte fill with 0 or `0xFF`; `0x0032EB2F`, `or 0x80`); `0x0032ED20` (`0x0032ED5E`, `or`; `0x0032ED64`, `and`) | `0x0032ED20` (`0x0032ED5E`, `0x0032ED64`, both read before they write) |
| `0x022C2680` | `u32` | 0 (zero-filled tail of `.data`) | `+0x08` of `0x00324510`'s request descriptor `0x022C2678`, the callback word: the low 32 bits of the address of the entry `0x022C27B8 + 8 × i` it requests | `0x00324510` (`0x00324631`) | `0x0032E870` (`0x0032E8E5`), through the descriptor `0x00324510` passes to `0x0032E620` (`0x00324637`); `0x0032E620` (`0x0032E678`, a 16-byte copy, taken while `0x003EB0D0()` is non-zero) |
| `0x022C2688` | `void*` | 0 (zero-filled tail of `.data`) | the descriptor's delivery callback `+0x10`, `0x003244F0` | `0x00324510` (`0x0032459C`) | `0x0032E870` (`0x0032E8DD`), through the descriptor `0x00324510` passes to `0x0032E620` (`0x00324637`); `0x0032E620` (`0x0032E67B`, the same copy) |
| `0x022C2690` | `void*` | 0 (zero-filled tail of `.data`) | the descriptor's cancel callback `+0x18`, `0x003244F0` | `0x00324510` (`0x00324590`) | `0x0032E870` (`0x0032E8E1`), through the descriptor `0x00324510` passes to `0x0032E620` (`0x00324637`); `0x0032E620` (`0x0032E67B`) |
| `0x022C3148` | `i32` | 0 (zero-filled tail of `.data`) | the index `i` of `0x00324510`'s next file: 0 when the build starts, one more after each file; the loop runs while `i` is below `0x12D` (301), a signed compare (`jge` at `0x00324578`, `jl` at `0x0032467A`) | `0x00324510` (`0x003245B2`, `0x00324672`) | `0x00324510` (`0x00324565`, `0x0032465C`) |
| `0x022C3150` | `void*` | 0 (zero-filled tail of `.data`) | `0x00324510`'s destination cursor in its buffer `[0x022C27B0]`: `+0x4BC` at the start, then advanced by each file's size rounded up to 4 (`0x00324654`-`0x00324669`). Each request gets it as its destination, and its offset from the buffer goes into the buffer's table (`0x00324617`-`0x00324622`) | `0x00324510` (`0x003245C2`, `0x00324669`) | `0x00324510` (`0x0032457E`, `0x0032463C`) |
| `0x02ADD178` | `void*` | 0 (zero-filled tail of `.data`) | record 0 `+0x08` of the sixteen `0x70`-byte records at `0x02ADD170`, its previous link. `0x00379D60` clears the records (`0x00379D99`) and links records 0 to 14 through `+0x00` (next) and `+0x08` (previous); the first pass stores the address `0x70` below record 0 here, then 0 | `0x00379D60` (`0x00379D99`, the clear; `0x00379DC7`, the first pass; `0x00379DF3`, 0) | no instruction names it |
| `0x02ADD800` | `void*` | 0 (zero-filled tail of `.data`) | record 15 `+0x00`, its next link: 0 | `0x00379D60` (`0x00379D99`; `0x00379DFA`, 0) | no instruction names it |
| `0x02ADD808` | `void*` | 0 (zero-filled tail of `.data`) | record 15 `+0x08`: record 14 (`0x02ADD790`). Record 14's own next link stays 0, so the chain from record 0 ends at record 14 | `0x00379D60` (`0x00379D99`; `0x00379E19`) | no instruction names it |
| `0x02ADD878` | `void*` | 0 (zero-filled tail of `.data`) | the qword after `0x02ADD870`, cleared before the records | `0x00379D60`, 0 (`0x00379D7D`) | no instruction names it |
| `0x02ADD880` | `void*` | 0 (zero-filled tail of `.data`) | record 0's address, `0x02ADD170` | `0x00379D60` (`0x00379E01`) | no instruction names it |
| `0x02ADD888` | `void*` | 0 (zero-filled tail of `.data`) | set to 0 | `0x00379D60`, 0 (`0x00379E0D`) | no instruction names it |

## Modding notes

- A request's offset is floored to a 2 KB boundary; a reader of a file at an unaligned offset gets the
  bytes from the boundary below.
- A request whose size entry is −1 is never read (`0x002DF7B0` tests the table entry, not the byte count); the queue completes it
  with the previous read's status, normally as delivered, with nothing written. A real read that fails
  calls nothing, and the slot is released.
- Cancelling a path request frees the path at once, even while its read is in flight; a second
  cancel of the same id before the pump finishes it frees the path again.

## Related

- [Bigfile archive](bigfile-archive.md): the archive behind path and kind reads.
- [File path resolution](file-path-resolution.md): how a path becomes bytes.
- [File size tables](file-size-tables-fst.md): where the kind and index sizes come from.
- [Music](../Sound-And-Music/music.md): the BGM stream that makes requests chunked.
