---
title: "File requests and the read queue: the request slots, how a load is queued, sized, read in parts and completed, and how a caller waits, asks or cancels"
kind: "system"
category: "Game files and data tables"
summary: "How the game asks for a file and gets it: the pool of 64 request slots and its pending and free lists, the builder that takes a kind and index or a path, the request id, the size lookup, the pump's six states from queued to delivered or failed, chunked reads of 512 KB parts while the BGM stream reader is armed, the delivery, failure and cancel callbacks, the full-queue stall, the drain and the asking form, the in-flight test and the cancel, which kinds the call sites pass, and the shipped constant requests."
addresses: "0032E450, 022C31C0, 022C51C0, 022C51C8, 022C51D0, 01EED498, 0032EA90, 022C51F0, 0032E400, 002DF960, 0032E620, 003EB0D0, 0032E870, 0032E990, 0032EC40, 0032E780, 0032E7C0, 0032E070, 0032E040, 0032E520, 0032E4D0, 0032E590, 0032E2F0, 0032E330, 0032E370, 0032E3B0, 0046E030, 002DF780, 002DF6C0, 0046DFE0, 0046E0E0, 0215EFF4, 0035E810, 022CA5E0, 0035EA30, 003EADD0, 02B5E0E0, 0046DD50, 003E9780, 003BB790, 0050DFE0, 00249180, 022C5AF0, 022C59F0, 0032EA50, 0032ECE0, 0032ED20"
---

## What the player sees

Every file the game loads during play, from a map's script set to a menu image, is a request in this
queue. When more than 64 loads are outstanding, the code asking for the next one stops and services
the queue until a slot frees up, which can lengthen a load.

## How it works

### The slots

`0032E450` builds 64 slots of `0x80` bytes at `022C31C0` at boot: each gets its index at `+0x58`,
id `+0x64` = −1, state word `+0x20` = 0 and `+0x28` = 0, and the slots are chained through `+0x10`
(next) and `+0x18` (previous) into the free list headed at `022C51D0`. The pending list's head and
tail (`022C51C0`, `022C51C8`) start empty and the request counter `01EED498` starts at 1.
`0032EA90` calls it, resets the BGM stream reader (`003EB050`) and zero-clears the 256 per-kind size
override pointers at `022C51F0`.

`0032E990(atTail)` takes the free head and links it into the pending list, at the tail when
`atTail` is non-zero and at the head otherwise. `0032EC40(slot)` unlinks a slot from the pending
list, pushes it on the free list and sets its id to −1. Neither clears the rest of the slot.

### Sizes

`0032E400(kind, index)` returns −1 for kind `0xFF`. When the override pointer for the kind is non-null
and the index is below `0x400`, it returns that table's dword as it is. Otherwise it asks `002DF960`
and rounds a positive result up to a multiple of 64. The override table's only static writer is
`0032EA90`'s zero-clear (its readers are `0032E400` and `0032EB40`), so every shipped size comes from
`002DF960`. A caller passes the size it gets as the request's byte count.

### Making a request

`0032E620(kind, index, dest, bytes, descriptor)` stores the kind and index in `022C51D8` /
`022C51DC` and returns −1 for a negative index.

- When the BGM stream reader is not armed (`003EB0D0`: byte `+0x31` of `02B5E0E0`), it calls
  `0032E870(kind, index, dest, bytes, descriptor, 1)` for the whole file.
- When it is armed, it copies the descriptor with `0x80000` in its second dword and, on a non-zero id,
  makes the request chunked: `+0x22` = 1, part cap `+0x30` = `0x80000`, remaining `+0x34` = bytes,
  first part `+0x28` = `min(bytes, 0x80000)`, `+0x50` = 0, `+0x00` = 0, and the offset `+0x2C`
  truncated again to a multiple of `0x800`.

`0032E780(kind, index, …)` refuses a negative index and otherwise calls `0032E870` directly; its
only caller is the BGM stream reader `003EADE0`. `0032E7C0(path, dest, bytes, descriptor)` copies the
path into arena 8 (`0036A190`) and requests it as kind `0xFF` with the low 32 bits of the copy's
address as the index.

`0032E870` first stalls while the free list is empty, calling the pump `0032E070(0)`, `0046DFE0` and
`0035EA30` in a loop. It then takes a slot at the tail of the pending list and fills it:

- `+0x24` index, `+0x21` kind, `+0x28` bytes, `+0x20` state 1;
- `+0x2C` the descriptor's first dword (the file offset) truncated toward zero to a multiple of
  `0x800` (`cdq`, `and edx, 0x7FF`, `add`, `and 0xFFFFF800`: a non-negative offset is floored);
- `+0x38` and `+0x70` the destination, `+0x40` and `+0x48` the descriptor's `+0x10` and `+0x18`,
  `+0x60` its `+0x08`, `+0x50` = 0, and `+0x00`, `+0x22` and `+0x5C` zeroed;
- the id `+0x64` = counter × 64 + slot index; the counter then advances and wraps from `0xFFFFFF`
  back to 1.

It returns the id. A null descriptor gives offset 0 and no callbacks.

### The pump

`0032E040` calls the pump `0032E070(0)` when `001EDE80()` or `001D6B70()` is non-zero. Its callers
are the main loop's mode bodies (`0022A770`, `0022AF50`, `0022B000`, `0022B6E0`, `0022B7E0`,
`0022B8C0`, `0022BC20`), boot `0022A0B0`, the script native `0036EEB0` and `00379E30`. The pump is
also run by the stall in `0032E870` and by the drain `0032E520(0)`.

The pump works on the pending head and keeps going while the head changes; a state that has to wait
ends the pass:

| State | Meaning | What the pass does |
|---|---|---|
| 1 | queued | if the BGM stream reader takes this pass (`003EADD0` returns 1), end the pass. A zero byte count: delivery callback, state 0, release. Kind `0xFF`: `002DF6C0(path, dest, bytes, offset)`, which always returns 0, then `+0x08` = `0035E810()` and state 2. Any other kind: `0046E030(kind, index, offset, bytes, dest)` → `002DF780`, then `+0x08` = `0035E810()` and state 2 |
| 2 | issued | `+0x00` += `0035E810()`, `+0x08` = the same value, state 3 |
| 3 | waiting | while the read status `0215EFF4` is −1 (`0046DFE0` returns 2), end the pass; otherwise state 5 when the status is 0 or more (`0046E0E0`), 6 when negative, and continue with that state |
| 4 | cancelled | while the read is in flight, end the pass; then the cancel callback with `+0x28` = 0 when one is set, state 0, release |
| 5 | delivered | not chunked: delivery callback and release. Chunked: remaining `+0x34` −= the part; when something is left, the offset `+0x2C` and destination `+0x38` advance by the part and the part callback decides; when nothing is left, delivery callback and release |
| 6 | failed | not chunked: failure callback and release. Chunked: failure callback and release |

In a chunked request a part-callback result of 1 sizes the next part as `min(+0x30, +0x34)`, zeroes
`+0x00`, truncates the offset to `0x800` again and requeues it in state 1; any other result is stored
at `+0x23` and ends the pass, and a stored 2 makes the next pass ask again. `0032E3B0` returns 1 when
no part callback is set, and the part callback slot `+0x50` is only ever written as 0 (`0032E6FF`,
`0032E959`), so in the shipped game every chunked request runs part after part.

`0035E810` returns the 64-bit tick counter `022CA5E0`, which only `0035EC90` increments (the callback
`0035E820` registers). Slot `+0x00` therefore sums counter readings; nothing reads it.

After the queue, every pass ends the same way: `0046DD50` (the read layer's tick), `003E9780`, and
`003BB790` when `0036FD50()` is non-zero. When the pending list is empty the pass also steps the
BGM stream reader (`003EADD0`) first.

### Callbacks

- **Delivery** `0032E330(slot)`: `+0x40(+0x60, +0x70, 1)` when set; for kind `0xFF`, frees the path
  (`003697F0`).
- **Failure** `0032E370(slot)`: `+0x40(+0x60, +0x70, 0)` only when the byte count `+0x28` is −1; then
  frees a kind-`0xFF` path. A failed read with any other byte count calls nothing, and a −1-size request
  reaches this only when the previous read had failed.
- **Cancel** `0032E2F0(slot)`: `+0x48(+0x60)` with `+0x28` = 0 when set, then state 0.

The first argument is the descriptor's `+0x08` word, not the buffer; a requester reads its bytes at
the destination.

### Waiting, asking and cancelling

- `0032E520(0)` drains: it pumps, and while the pending list is non-empty or a read is in flight it
  waits (`0035EA30`) and pumps again. `0032E520` with a non-zero argument only answers 1 when the
  pending list is non-empty or a read is in flight, without pumping.
- `0032E4D0(id)` answers 1 when the slot `id & 0x3F` still carries that id and a non-zero state; 0 and
  −1 are refused.
- `0032E590(id)` cancels a request whose slot still carries the id: it clears the delivery callback
  `+0x40` and frees a kind-`0xFF` path at once; a request in states 2 or 3 goes to state 4 for the
  pump to finish; state 4 is left alone; any other state runs the cancel callback and is released at
  once. Its callers are `002FC3C0`, `003B1310`, `003B1710` and `003B18E0`.

`0035EA30(n)` is `0035EB70(n, 0)`: off the thread `00368C70` names it spins until the tick counter
has advanced by `max(n, 1)`; on that thread it only updates the frame bookkeeping and does not wait.

### The BGM stream reader

`003EADD0` steps the BGM stream reader, whose state lives at `02B5E0E0` (`+0x31` active, `+0x30` state 1-8), which
files its own requests through `0032E780`. It returns 1 only in states 1 and 7, on the call where it
submits, and 0 when inactive, while waiting (states 2 and 8 test its request with `0032E4D0`, state 4
tests `002DEE90`) and when it finishes. The pump's state 1 gives up the pass when it returns 1, so the
reader's request goes first.

Only `003EB100` arms the reader (kind `0x24`, index = its argument, `+0x30` = 1, `+0x31` = 1, and only
when its buffer `+0x08` exists); its only caller is `bgmstreamread` (`0x0448`, `00354690`). `003EB010`
releases it (`003EAD10`, then frees `+0x08`; callers `usebgmstream` `003557C0` and `002628B0`),
`003EB050` resets it at init (from `0032EA90`), and `003EB0D0` is the query (callers `0032E620`,
`bgmstreamplaysync` `003550F0` and `getbgmstreamstatus` `00355FB0`).

Of the 10,036 decompiled
scripts, only the two ATEL control scripts `ps2data_image_ff12_ch_bin_ctrl` and
`ps2data_image_ff12_in_bin_ctrl` use the BGM stream verbs, so in normal play the reader is never
armed, no request is chunked, and `003EADD0` never takes a pass. Kind `0x24` is also one of the
unsized kinds of the size table.

### The read-source switches

Two 256-byte bit tables, one bit per resource kind, survive from the PS2 build: `022C5AF0` (read from
the hard disk) and `022C59F0` (read from the PC). Boot (`0022A0B0` → `003694D0`) clears both
(`0032EAF0(0)`, `0032EB10(0)`); `0032EB10` then sets kind `0xFF`'s bit in the PC table.

| Verb | Native | Body |
|---|---|---|
| `getreadfromhdd` `0x037A` | `00342DD0` | `0032EA50(kind)`: the kind's bit in `022C5AF0` |
| `setreadfromhdd` `0x0379` | `00342960` | `0032ECE0(kind, flag)`: sets or clears the kind's bit in `022C5AF0` |
| `setreadfrompc` `0x0377` | `003420B0` | `0032ED20(kind, flag)`: the same in `022C59F0`; kind `0xFF` is always set |

Nothing else reads either table: the builder, the pump and the read issuer route every request the same
way whatever the bits say.

### Which kinds are requested

`0032E620` has 51 call sites in 38 functions. 38 pass a fixed kind: an immediate, a constant folded
through a register, one of a closed set (`002FC96F`: `0xB` or `0x26`; `0032FCA0`: 5, 8, 1 or `0x25`),
or a kind from `002ED6F0`'s class table, none of them `0xFF`. Nine pass a caller's parameter and three
a signed word of a record (a word of −1 sign-extends to −1, which the builder refuses first).
`debug_fileread` (`0x2007`, `0050DFE0`) passes a kind popped from the script.

## Layouts

```
slot (0x80)   +0x00 u64 counter sum, +0x08 u64 counter at issue, +0x10 next, +0x18 prev,
              +0x20 u8 state, +0x21 u8 kind, +0x22 u8 chunked, +0x23 u8 part result, +0x24 s32 index (or path),
              +0x28 s32 bytes (current part), +0x2C s32 file offset, +0x30 s32 part cap, +0x34 s32 remaining,
              +0x38 destination (current part), +0x40 delivery/failure callback, +0x48 cancel callback,
              +0x50 part callback, +0x58 u32 slot index, +0x5C u32, +0x60 u32 callback word, +0x64 u32 id,
              +0x70 destination (start)
descriptor    +0x00 s32 file offset, +0x08 u32 callback word, +0x10 delivery/failure callback, +0x18 cancel callback
queue         022C51C0 pending head, 022C51C8 pending tail, 022C51D0 free head, 022C51D8 kind, 022C51DC index,
              022C51F0 256 size override pointers, 01EED498 request counter
read status   0215EFF4: -1 in flight, >= 0 delivered, other negative failed
```

The fields are listed access by access in
[`file-requests-and-the-read-queue-slot-accesses.tsv`](file-requests-and-the-read-queue-slot-accesses.tsv),
[`file-requests-and-the-read-queue-read-status-accesses.tsv`](file-requests-and-the-read-queue-read-status-accesses.tsv) and
[`file-requests-and-the-read-queue-size-override-accesses.tsv`](file-requests-and-the-read-queue-size-override-accesses.tsv).

## Shipped data

[`file-requests-and-the-read-queue-constant-requests.tsv`](file-requests-and-the-read-queue-constant-requests.tsv)
lists 238 call sites of the request and size entries (`0032E620` 65, `0032E400` 86, `00249210` 52,
`002493D0` 21, `00249180` 11, `0032E3F0` 2, `00249350` 1) with the kind, id and file name where they
are constant. 203 sites carry a constant kind: 121 of kind 7, 34 of kind 9, 18 path requests
(`0xFF`), 8 of kind 5 and 22 over eleven other kinds. No decompiled script in any locale calls
`debug_fileread`.

## Operations

Per request: one slot, one read (or one per 512 KB part while the BGM stream reader is armed) and one
callback.
Per pump pass: as many state steps as the pending head allows before a wait.

## State

The 64 slots and the three list heads, the request counter, the read status word `0215EFF4`, the tick
counter `022CA5E0` and the BGM stream reader at `02B5E0E0`.

## Modding notes

- A request's offset is floored to a 2 KB boundary; a reader of a file at an unaligned offset gets the
  bytes from the boundary below.
- A request whose size entry is −1 is never read (`002DF780` does nothing); the queue completes it
  with the previous read's status, normally as delivered, with nothing written. A real read that fails
  calls nothing, and the slot is released.
- Cancelling a path request frees the path at once, even while its read is in flight; a second
  cancel of the same id before the pump finishes it frees the path again.

## Related

- [Bigfile archive](bigfile-archive.md): the archive behind path and kind reads.
- [File path resolution](file-path-resolution.md): how a path becomes bytes.
- [File size tables](file-size-tables-fst.md): where the kind and index sizes come from.
- [Music](../Sound-And-Music/music.md): the BGM stream that makes requests chunked.
