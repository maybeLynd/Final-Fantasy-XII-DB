---
title: "Asynchronous load manager: the loading thread, its request records, the four load kinds and the .efx appendix"
kind: "system"
category: "Game files and data tables"
addresses: "0x01F81160, 0x001A11B0, 0x001A1220, 0x0019F620, 0x001A0AF0, 0x0019F490, 0x0019FFD0, 0x001A0A90, 0x001A0BB0, 0x001A0C50, 0x001A1230, 0x001A07B0, 0x001A0CF0, 0x001A0E50, 0x001A0F80, 0x001A09E0, 0x001A1310, 0x001A0960, 0x0019F930, 0x002DF780, 0x001D6D90, 0x001D6FB0, 0x001D6EF0, 0x001D6B40, 0x001BA860, 0x002124C0, 0x005CC900, 0x005CC8A0"
---

## What the player sees

The game keeps drawing while it loads. Remastered models, maps, textures, fonts and the text lists that
name them, and the PS2-era files the game logic asks for, are mostly read on a separate loading thread, and
the code that asked is told on a later run of the completion pump that the data is there. When a summon, a
monster or an NPC model is read, the game also reads that model's character effect file and hands both over as one
block.

A request filed with `now` set runs at once on the calling thread instead, and a record with byte `+0x18`
set calls back on the thread that ran it, not from the completion pump: a PS2-era file the RAM cache already holds
is read that way, and its callback has run when the read returns (`0x001D7028`, `0x001D7076`).

## How it works

### The manager

`0x001A11B0` builds the manager once: it allocates `0x140228` bytes (`0x00584740`), constructs them with `0x0019F620` and
stores the object at `0x01F81160`; `0x001A1220` returns it. It is called from `0x0017D4C0` (`0x0017D56C`); it returns at once
while `0x01F81160` is set (`0x001A11C5`), runs `0x0019F620` only on a non-null block, and stores 0 when the allocation fails
(`0x001A11D9`, `0x001A11E4`).

The constructor zeroes the thread record `+0x08` (`0x005CC900`, `0x0019F63F`) and the started byte `+0x20` (`0x0019F644`),
installs the `AsyncLoadManager` vtable `0x008F46F0` (`0x0019F64F`), sets up the queue, the completion vector and three
locks, builds the record pool (`0x0019F490(manager + 0xB8, 0x400, 0)`: 1,024 records of `0x140` bytes, `0x0019F6C6`),
calls `0x001A0AF0` (`0x0019F6DB`) and returns the manager (`0x0019F6E1`).

`0x001A0AF0` empties the queue (`0x002218D0`, `0x001A0AFD`), creates the queue lock's event (`0x005CD0A0`, `0x001A0B06`),
marks the queue empty (`+0x68` = 1) and the thread idle (`+0x69` = 1) with one 16-bit store of `0x101` (`0x001A0B12`),
empties the completion vector (end = begin, `0x001A0B20`) and reserves 32 completion entries (`0x001A1050`, which moves
them to a new block with `0x0019F060`). It creates the events of the completion lock `+0x70` and the pool lock
`+0x178` (`0x005CD0A0`, `0x001A0B2D`, `0x001A0B39`) and fills the `.efx` appendix table (`0x0019FFD0`).

It then fills a thread block (`0x005CC8C0`) with the entry `0x001A1230`, a 64 KB stack, the priority selector 2 and the
name `AsyncLoadManager`, hands the block and `0x7C` to the return stub `0x0016D6A0` (`0x001A0B7D`), which does nothing,
and stores the manager as the thread's argument (`0x001A0B87`). It sets the run byte `+0x1A0` to 1 (`0x001A0B90`)
before it starts the thread on the record `+0x08` (`0x005CD1E0`, `CreateThread`, `0x001A0B97`), and sets the started
byte `+0x20` to 1 after (`0x001A0B9C`).

The locks are PhyreEngine mutexes: `0x005CD4F0` takes one (`0x005CD450`: an atomic flag, with
`WaitForSingleObject` on the lock's event while it is held), `0x005CD820` releases it and signals the
event (`0x005CD570`) when a thread is waiting.

### The record pool

A pool is a vector of fixed records with a free set `+0x20` and a used set `+0x58`, each an ordered tree of record
addresses; `0x0019F490` sizes the vector (`0x001A1130`, `0x0019F59B`) and puts every record's address in the free set
(`0x00199DB0`, `0x0019F5D2`). `0x001BA860(pool)` takes the lowest free record, moves it to the used set and returns it, or
returns 0 when no record is free; `0x002124C0(pool, record)` moves a record back.

`0x002124C0` looks the record up in the used set (`0x00212500`-`0x0021252C`) and, when it is not there, changes nothing.
A pool built with its lock byte set takes its own lock around both, and `0x0019F490` creates that lock's event
(`0x005CD0A0`, `0x0019F5F5`); the manager's pool is built without one and the manager guards it with its lock `+0x178`
instead.

`0x001A0A90(manager)` takes a record under that lock, zeroes its `+0x128` and returns it. It does not test the
record: with no record free, `0x001BA860` returns 0 and the store goes to address `0x128`, which faults (`0x001A0ACB`).
The record vector grows through `0x0019FC30` and `0x001A1130`; `0x0019F0D0`, `0x0019F250`, `0x0019F300` and `0x0019F3E0` copy
and fill `0x140`-byte records, and `0x0019F6F0` destroys the pool.

### Queuing a request

A caller fills the record (kind, callback, argument, the thread byte, the path) and files it:

- `0x001A0BB0(manager, record, now)` puts it at the head of the queue;
- `0x001A0C50(manager, record, now)` puts it at the tail.

Both ignore a record of kind 0 (`0x001A0BD4`, `0x001A0C74`), take the queue lock `+0x28`, link a `0x18`-byte list node
holding the record and clear the empty byte `+0x68`. The node comes from the list allocator `+0x60` (slot 2,
`_aligned_malloc`) and is used without a null test: a null node faults on the store to address `0x10`
(`0x001A0C15`, `0x001A0CB5`). With `now` set they skip the queue and run the request at once on the calling thread
(`0x001A07B0`, `0x001A0BDE`, `0x001A0C7E`).

The loading thread takes from the tail, so `0x001A0BB0` requests run in the order they were filed and a
`0x001A0C50` request runs before everything already waiting. Several `0x001A0C50` requests run in reverse
order among themselves, since each new one is the next taken.

### The loading thread

The body at `0x001A1230` (`0x001A1240`) loops while the run byte is set. With the queue empty it sets the
idle byte `+0x69` and sleeps 1 ms (`0x005CCB80`). Otherwise it clears the idle byte, unlinks the tail node
under the queue lock, sets the empty byte when the queue is now empty, and runs the request with
`0x001A07B0`.

`0x001A07B0(manager, record)` brackets the work with `0x0017D940(0)` and `0x0017D960(0)`, which raise and
lower the prefetch manager's busy counter and stamp its last-activity time, so the prefetch worker
stands back while a load runs. It then does the kind's work (kinds 1 to 4; any other kind does no load
work, `0x001A07EA`), delivers the completion and returns the record to the pool under `+0x178`
(`0x002124C0`, `0x001A08C3`); `0x0017D960(0)` is a tail jump (`0x001A08E3`).

### The four kinds

| Kind | Body | What it does |
|---|---|---|
| 1 | `0x0019CB20` | loads the `.phyre` file at `+0x20` through the asset manager (`0x0019CE20()`, then `0x0019CB20(asset manager, record + 0x20, 0)`), stores the result at `[+0x120]` with no null test of `+0x120`, so a null `+0x120` faults (`0x001A082E`), and, when `+0x128` is set, writes 1 to the byte it points to |
| 2 | `0x001A0CF0` | opens `+0x20` (selector 1), seeks to the offset `+0x128` (its low 32 bits, `0x001A0D4C`) before it tests the open (`0x0059D920`, `0x001A0D61`), reads `+0x130` bytes (or the file's size, `0x001FDF70`, when that 64-bit word is `FFFFFFFF`, `0x001A0D2B`-`0x001A0D41`) into `+0x120`, and puts the byte count, or `FFFFFFFE` when the file did not open, in `+0x10` (`0x001A0D87`); it then closes the stream (`0x0059BD40`, `0x001A0D90`) and, after the appendix step, destroys it (`0x00598100`, `0x001A0E32`) |
| 3 | `0x001A0E50` | the same read from the already open stream at `+0x138`, which it leaves open |
| 4 | `0x001A0F80` | reads the whole file (the stream's size word `+0x1C` less its position `+0x18`, `0x001A0FCD`-`0x001A0FD6`) into a new block one byte longer (`malloc`, `0x0085E730`), zero-terminates it, stores the block at `[+0x120]` and, when `+0x128` is set, the end at `[+0x128]`; an unopened file stores 0 (`0x001A0FC4`). Neither store through `+0x120` tests it for null, and the block is not tested: a null block is passed to the read (`0x001A0FFD`) and the terminator goes to the address equal to the size (`0x001A1008`), which faults for a size below `0x10000` |

Kinds 2 and 3 overwrite the argument with the byte count, so their callback receives the count. An
empty file in kind 4 stores nothing, leaving the caller's pointer as it was.

### Finishing a request

With the record's byte `+0x18` set, the callback `+0x08` runs at once with the argument `+0x10`, on the thread
running `0x001A07B0`: the loading thread for a queued request, the filing thread for one filed with `now` set
(`0x001A0846`-`0x001A0853`); a null callback is skipped (`0x001A084D`). Otherwise `0x001A07B0` appends
`{callback, argument, byte}` to the completion vector `+0x98` under the lock `+0x70` (growing it with `0x0019FA50`
when full); the entry's third word is the record's whole qword at `+0x18`, the byte and the seven bytes after it
(`0x001A0889`).

Each pass of the frame pump `0x0017D6E0` runs `0x001A1310(manager)` (`0x0017D790`): under the same lock it copies the
vector to the stack and empties it, then calls every non-null callback with its argument on the main thread.

A callback that files a new request with byte `+0x18` clear therefore sees that request's callback no earlier than
a later run of `0x001A1310`, the first one after the completion is queued. That run is not always in a later frame,
because `0x0017D6E0` can make a second pass in one call
([the game application](../Engine-Core/game-application.md)). The file being read and its callback
running are separate events. With the byte set, the new request's callback runs on the thread that ran it
(`0x001A0846`-`0x001A0853`), before the filing call returns when `now` is set.

### PS2 file reads

The read issuer `0x002DF780(kind, id, dest, bytes, offset)` first reads the size table word
`0x02EC3EE0[kind × 5000 + id]`: when it is −1 it returns 0 without reading or queuing anything and leaves
the read status `0x0215EFF4` as it was. It returns 0 on every path (`0x002DF862`). Otherwise it takes the path
`0x0215F000[kind][id]` (`0x002DF7BF`, `0x002DF7CC`), with no null test of the kind's array or of the entry.

Otherwise it, and its by-path twin `0x002DF6C0` (which has no such
test), read directly when three things hold: the prefetch manager's byte `+0x88` is set (`0x001D6B70`), the loader is idle with an empty
queue (`0x001D6EF0`: `+0x69` and `+0x68`), and the RAM file cache already holds the name (`0x001D6B40`).
Then it opens the file (`0x001D6F20`), runs a kind 3 request at once (`0x001D6FB0`, `now` = 1) and closes
and frees the stream (`0x001D6E80`). When that open fails it reads nothing and sets no status.

Otherwise it queues a kind 2 request (`0x001D6D90`) at the head. Both builders return at once, issuing nothing and
leaving the status as it was, when no manager exists (`0x001A1220` returns 0; `0x001D6DB9`, `0x001D6FD9`) or the status
pointer is null (`0x001D6DC7`, `0x001D6FE7`). Otherwise they set the read status `0x0215EFF4` to −1, point `0x01F82CC0` at
it, take a record (`0x001A0A90`), set its callback `0x001D6D70`, argument 0 and byte `+0x18` = 1, and copy the path to
`+0x20` up to its terminator with no length limit (`0x001D6E20`-`0x001D6E2D`, `0x001D7040`-`0x001D704D`).

They store the destination `+0x120`, the offset as the low 32 bits of `+0x128` and the byte count as the 64-bit
`+0x130`; `0x001D6FB0` also stores the stream `+0x138` (`0x001D7064`). The kind 2 record runs later on the loading
thread. The kind 3 record runs at once on the calling thread (`0x001A0BB0` with `now` = 1, `0x001D7076`-`0x001D707C`),
so its callback has run when `0x001D6FB0` returns.

The callback `0x001D6D70` writes the byte count through `0x01F82CC0` and clears it. `0x002DF880(kind, id, buffer,
n)` copies the same path into a buffer, at most n characters and a terminator, and returns −1 for an id
with no path.

Its one caller, the map-pack loader `0x00377DC0`, takes the file name from that path to
build the loose effect bank path `PS2Data\efb\<name>.efb`
([MPK map pack](../World-Areas-And-Travel/mpk-map-pack.md)).

`0x001D6B40(name)` asks the cache (`0x0020BE50`): it drops a leading `/hostapp/`, `/app0/` or `/host/`,
builds the cache key (`0x0020C440`), hashes it (`0x00674A00`) and searches the cache's tree under its lock,
returning 1 on a hit.

### The .efx appendix

After a kind 2 or 3 read, when the stored count n is above 0 (kind 2, a signed 64-bit test that the
failure value `FFFFFFFE` also passes) or non-zero (kind 3), `0x001A09E0(manager, path)` checks for a name of more than eight characters ending `.cm`, such as `...\m1006.cm`. When the byte
for the eighth character from the end is set in the table `+0x1A1`, and the four characters after it,
read as decimal digits, give a number below 1,280, it returns the path stored for that character and
number in the table `+0x228`; otherwise it returns 0 (`0x001A0A88`).

The character is sign-extended (`0x001A0A20`), so a byte of `0x80` or above indexes the 128 bytes below the table
`+0x1A1`. The four characters are not tested as digits: the number is the sum of each code less `0x30`,
`c - 0x30`, times 1,000, 100, 10 and 1, `n = (c1 - 0x30) * 1000 + (c2 - 0x30) * 100 + (c3 - 0x30) * 10 + (c4 - 0x30)`,
computed as `10 * (10 * (10 * c1 + c2) + c3) + c4 - 0xD050` (`0x001A0A30`-`0x001A0A69`), and only the unsigned test
against 1,280, `n < 0x500` (`0x001A0A6D`), bounds it.

For a path it opens that file (selector 1), takes its size by seeking to the end, reads the whole
file into the destination right after the n bytes, and writes n as a `u32` in the last four bytes of the
requested length (`+0x130`, or the stream size). The block then holds the model, its effect file and,
at its end, where the model stops.

It closes the effect file's stream afterwards (`0x0059BD40`; `0x001A0E0F`, `0x001A0F42`) and does not test that the file
opened. After a failed kind 2 open n is `FFFFFFFE`, so the effect file is read to the destination plus `FFFFFFFE`
and `FFFFFFFE` is the `u32` written (`0x001A0DF0`, `0x001A0E1B`).

`0x0019FFD0` clears both tables, enables the letters `g`, `m`, `n` and `s`, and stores 144 paths of the
form `PS2Data\effect_finish\jp\chara\hNNNN.efx`.

### Shutting down

`0x001A0960` clears the run byte, waits for the thread to end (`0x005CD330`), frees the queue's nodes
(`0x002218D0`), marks it empty, drops pending completions (end = begin, `0x001A099A`), and closes the three locks'
events (`0x005CD6D0`). It then calls the return-zero stub `0x005C5230` on the thread record (`0x001A09BF`), which does
nothing, and clears the started byte `+0x20` (`0x001A09C4`).

The destructor `0x0019F930` reinstalls the `AsyncLoadManager` vtable (`0x0019F953`), calls it and then destroys the
pool (`0x0019F6F0`), frees the completion vector's block through its allocator `+0xB0` when its begin is non-null
(`0x0019F970`-`0x0019F9AF`), and frees any list nodes left through the list allocator `+0x60` (`0x0019F9C0`-`0x0019F9DB`).
This body does not free the manager's own block.

## Layouts

### Manager

`0x140228` bytes at `[0x01F81160]`.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `void*` | vtable | `AsyncLoadManager` |
| `+0x008` | `Thread` | thread | the thread record of [runtime services](../Compiler-And-C-Runtime/runtime-services.md) (handle, start, argument; zeroed by `0x005CC900`), started by `0x001A0AF0` |
| `+0x020` | `u8` | started | |
| `+0x028` | `PhyreLock` | queue lock | the PhyreEngine lock of [runtime services](../Compiler-And-C-Runtime/runtime-services.md), built by `0x005CC8A0` |
| `+0x050` | `List` | queue | an EASTL list: the anchor's next and previous (the tail) at `50` and `58`, its allocator at `60` built by `0x001EDF00`, which drops the name `EASTL list` it is passed (`0x0019F678`); `0x18`-byte nodes, the record at node `10` |
| `+0x068` | `u8` | queue empty | |
| `+0x069` | `u8` | thread idle | |
| `+0x070` | `PhyreLock` | completion lock | the PhyreEngine lock, built by `0x005CC8A0` |
| `+0x098` | `Vector` | completions | an [EASTL vector](../Third-Party-Libraries/eastl-strings-and-containers.md): begin, end at `A0`, capacity at `A8`, allocator at `B0`; completion entries |
| `+0x0B8` | `RecordPool` | requests | the pool template of [game application](../Engine-Core/game-application.md) (`0x0019F490`): vector at `+0`, sets at `+0x20` and `+0x58`, lock at `+0x90`, flag `+0xB8` 0 here; 1,024 request records |
| `+0x178` | `PhyreLock` | pool lock | the PhyreEngine lock, built by `0x005CC8A0` |
| `+0x1A0` | `u8` | run | |
| `+0x1A1` | `u8[128]` | letter enable | indexed by the character code |
| `+0x228` | `char*[163840]` | appendix paths | `[character × 1280 + number]`, the `.efx` path or null |

### Request record

`0x140` bytes.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u32` | kind | `1` asset, `2` read by name, `3` read from a stream, `4` whole text |
| `+0x008` | `void*` | callback | |
| `+0x010` | `u64` | argument | kinds 2 and 3: replaced by the byte count |
| `+0x018` | `u8` | complete on thread | `1` = call at once on the thread running the request (the loading thread, or the filing thread for a request filed with `now` set, `0x001A0846`-`0x001A0853`), `0` = next pump |
| `+0x020` | `char[256]` | path | |
| `+0x120` | `void*` | result | kinds 1 and 4: where to store; kinds 2 and 3: the destination |
| `+0x128` | `u64` | second | kind 1: done byte pointer; kinds 2 and 3: file offset, read and written as its low 32 bits (`0x001A0D4C`, `0x001A0EA4`, `0x001D6E36`, `0x001D7061`); kind 4: end pointer |
| `+0x130` | `u64` | byte count | kinds 2 and 3, read and written as 64 bits (`0x001A0D2B`, `0x001A0E85`, `0x001D6E3C`, `0x001D7053`); `FFFFFFFF` = the whole file |
| `+0x138` | `void*` | stream | kind 3 |

### Completion entry

`0x18` bytes.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | callback | |
| `+0x08` | `u64` | argument | |
| `+0x10` | `u64` | on thread | the record's qword at `18`: its byte `18` and the seven bytes after it (`0x001A0889`); `0x001A1310` does not read it |

## Shipped data

| Fact | Value |
|---|---|
| appendix entries | 144: `m` 82, `n` 27, `s` 26, `g` 9 |
| appendix files | 125 distinct `.efx`; `h0024.efx` is named 7 times, thirteen others twice |
| doubled summon effects | the thirteen summons `s0002`–`s0015` other than `s0008` and the thirteen `s0019`–`s0031` take the same thirteen files, in the same order |
| models | all 144 name an existing `ps2data/obj_finish/in/.../<letter><nnnn>.cm` |
| file size table | for all 144 the US `.fst` size is exactly model + effect + 4 |

## Operations

Per request: one record from the pool, one list node, one file open (two with an appendix), and one
completion entry when the callback is deferred. The loading thread polls an empty queue every 1 ms.

## State

The manager at `0x01F81160` with its queue, completion vector, record pool, the run, idle and empty
bytes, and the appendix tables, which nothing but `0x0019FFD0` writes. The read status `0x0215EFF4` and
its pointer `0x01F82CC0` for PS2 file reads.

## Modding notes

- At most 1,024 requests can be outstanding; with no record free, `0x001BA860` returns 0, and `0x001A0A90` stores 0 at
  `+0x128` of that null record without a test, which faults at address `0x128` (`0x001A0ACB`); its callers write the
  kind through the record without a test as well.
- The appendix is fixed in the executable: a model listed there always gets its effect file appended,
  so its size table entry must cover the model, the effect and 4 bytes. A model not listed gets
  nothing appended.
- Replacing an appended `.efx` changes the total; update that model's size in every `.fst`.
- A callback on a queued request with byte `+0x18` clear runs at the first run of `0x001A1310` after the completion is
  queued, not when the file arrives. One frame can hold two such runs.

## Related

- [File requests and the read queue](file-requests-and-the-read-queue.md): the PS2 request slots whose reads come here.
- [File size tables](file-size-tables-fst.md): the sizes the PS2 reads ask for.
- [Texture animation lists](texture-animation-lists-ta.md): one of the text lists read as kind 4.
- [Fonts](../Menus-And-HUD/fonts.md): the font lists and files read through this queue.
- [PhyreEngine asset files](../PhyreEngine/phyre-asset-files.md): what a kind 1 load does with the file.
- [Model files](../Graphics/model-files-cm-ca.md): the `.cm` files the appendix extends.
- [Effect files](../Graphics/effect-files-efx-efb.md): the `.efx` files it appends.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Developer: `0x0017D6E0` calls `0x001C2F50`; those functions are documented on
  [game application](../Engine-Core/game-application.md).
