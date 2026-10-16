---
title: "Asynchronous load manager: the loading thread, its request records, the four load kinds and the .efx appendix"
kind: "system"
category: "Game files and data tables"
addresses: "01F81160, 001A11B0, 001A1220, 0019F620, 001A0AF0, 0019F490, 0019FFD0, 001A0A90, 001A0BB0, 001A0C50, 001A1230, 001A07B0, 001A0CF0, 001A0E50, 001A0F80, 001A09E0, 001A1310, 001A0960, 0019F930, 002DF780, 001D6D90, 001D6FB0, 001D6EF0, 001D6B40, 001BA860, 002124C0, 005CC900, 005CC8A0"
---

## What the player sees

The game keeps drawing while it loads. Remastered models, maps, textures, fonts and the text lists that
name them, and the PS2-era files the game logic asks for, are read on a separate loading thread; the
code that asked is told in a later frame that the data is there. When a summon, a monster or an NPC
model is read, the game also reads that model's character effect file and hands both over as one
block.

## How it works

### The manager

`001A11B0` builds the manager once: it allocates `0x140228` bytes (`00584740`), constructs them with
`0019F620` and stores the object at `01F81160`; `001A1220` returns it. The constructor installs the
`AsyncLoadManager` vtable, sets up the queue, the completion vector and three locks, builds the record
pool (`0019F490(manager + 0xB8, 0x400, 0)`: 1,024 records of `0x140` bytes) and calls `001A0AF0`.

`001A0AF0` marks the queue empty (`+0x68` = 1) and the thread idle (`+0x69` = 1), reserves 32
completion entries (`001A1050`, which moves them to a new block with `0019F060`), fills the `.efx` appendix table (`0019FFD0`), starts a thread named
`AsyncLoadManager` at `001A1230` with a 64 KB stack (`005CD1E0`, `CreateThread`), and sets the run byte `+0x1A0` and the started byte
`+0x20`.

The locks are PhyreEngine mutexes: `005CD4F0` takes one (`005CD450`: an atomic flag, with
`WaitForSingleObject` on the lock's event while it is held), `005CD820` releases it and signals the
event (`005CD570`) when a thread is waiting.

### The record pool

A pool is a vector of fixed records with a free set and a used set, each an ordered tree of record
addresses. `001BA860(pool)` takes the lowest free record, moves it to the used set and returns it, or
returns 0 when none is free; `002124C0(pool, record)` moves a record back. A pool built with its lock
byte set takes its own lock around both; the manager's pool is built without one and the manager
guards it with its lock `+0x178` instead.

`001A0A90(manager)` takes a record under that lock and zeroes its `+0x128`. The record vector grows
through `0019FC30` and `001A1130`; `0019F0D0`, `0019F250`, `0019F300` and `0019F3E0` copy and fill
`0x140`-byte records, and `0019F6F0` destroys the pool.

### Queuing a request

A caller fills the record (kind, callback, argument, the thread byte, the path) and files it:

- `001A0BB0(manager, record, now)` puts it at the head of the queue;
- `001A0C50(manager, record, now)` puts it at the tail.

Both ignore a record of kind 0, take the queue lock `+0x28`, link a `0x18`-byte list node holding the
record and clear the empty byte `+0x68`. With `now` set they skip the queue and run the request at once
on the calling thread (`001A07B0`).

The loading thread takes from the tail, so `001A0BB0` requests run in the order they were filed and a
`001A0C50` request runs before everything already waiting. Several `001A0C50` requests run in reverse
order among themselves, since each new one is the next taken.

### The loading thread

The body at `001A1230` (`001A1240`) loops while the run byte is set. With the queue empty it sets the
idle byte `+0x69` and sleeps 1 ms (`005CCB80`). Otherwise it clears the idle byte, unlinks the tail node
under the queue lock, sets the empty byte when the queue is now empty, and runs the request with
`001A07B0`.

`001A07B0(manager, record)` brackets the work with `0017D940(0)` and `0017D960(0)`, which raise and
lower the prefetch manager's busy counter and stamp its last-activity time, so the prefetch worker
stands back while a load runs. It then does the kind's work, delivers the completion and returns the
record to the pool under `+0x178`.

### The four kinds

| Kind | Body | What it does |
|---|---|---|
| 1 | `0019CB20` | loads the `.phyre` file at `+0x20` through the asset manager (`0019CE20()`), stores the result at `[+0x120]` and, when `+0x128` is set, writes 1 to the byte it points to |
| 2 | `001A0CF0` | opens `+0x20` (selector 1), seeks to the offset `+0x128`, reads `+0x130` bytes (or the file's size when that is `FFFFFFFF`) into `+0x120`, and puts the byte count, or `FFFFFFFE` when the file did not open, in `+0x10` |
| 3 | `001A0E50` | the same read from the already open stream at `+0x138`, which it leaves open |
| 4 | `001A0F80` | reads the whole file into a new block one byte longer, zero-terminates it, stores the block at `[+0x120]` and, when `+0x128` is set, the end at `[+0x128]`; an unopened file stores 0 |

Kinds 2 and 3 overwrite the argument with the byte count, so their callback receives the count. An
empty file in kind 4 stores nothing, leaving the caller's pointer as it was.

### Finishing a request

With the record's byte `+0x18` set, the callback `+0x08` runs on the loading thread with the argument
`+0x10`. Otherwise `001A07B0` appends `{callback, argument, byte}` to the completion vector `+0x98`
under the lock `+0x70` (growing it with `0019FA50` when full).

Each frame the pump runs `001A1310(manager)`: under the same lock it copies the vector to the stack and
empties it, then calls every non-null callback with its argument on the main thread. A callback that
files a new request therefore sees it finish in a later frame.

### PS2 file reads

The read issuer `002DF780(kind, id, dest, bytes, offset)` first reads the size table word
`02EC3EE0[kind × 5000 + id]`: when it is −1 it returns 0 without reading or queuing anything and leaves
the read status `0215EFF4` as it was.

Otherwise it, and its by-path twin `002DF6C0` (which has no such
test), read directly when three things hold: the prefetch manager's byte `+0x88` is set (`001D6B70`), the loader is idle with an empty
queue (`001D6EF0`: `+0x69` and `+0x68`), and the RAM file cache already holds the name (`001D6B40`).
Then it opens the file (`001D6F20`), runs a kind 3 request at once (`001D6FB0`, `now` = 1) and closes
and frees the stream (`001D6E80`). When that open fails it reads nothing and sets no status.

Otherwise it queues a kind 2 request (`001D6D90`) at the head. Both builders set the read status
`0215EFF4` to −1, point `01F82CC0` at it and mark the record to complete on the loading thread; the
callback `001D6D70` writes the byte count through `01F82CC0` and clears it. `002DF880(kind, id, buffer,
n)` copies the same path into a buffer, at most n characters and a terminator, and returns −1 for an id
with no path.

`001D6B40(name)` asks the cache (`0020BE50`): it drops a leading `/hostapp/`, `/app0/` or `/host/`,
builds the cache key (`0020C440`), hashes it (`00674A00`) and searches the cache's tree under its lock,
returning 1 on a hit.

### The .efx appendix

After a kind 2 or 3 read, when the stored count n is above 0 (kind 2, a signed 64-bit test that the
failure value `FFFFFFFE` also passes) or non-zero (kind 3), `001A09E0(manager, path)` checks for a name of more than eight characters ending `.cm`, such as `...\m1006.cm`. When the byte
for the eighth character from the end is set in the table `+0x1A1`, and the four characters after it,
read as decimal digits, give a number below 1,280, it returns the path stored for that character and
number in the table `+0x228`.

For a path it opens that file (selector 1), takes its size by seeking to the end, reads the whole
file into the destination right after the n bytes, and writes n as a `u32` in the last four bytes of the
requested length (`+0x130`, or the stream size). The block then holds the model, its effect file and,
at its end, where the model stops.

`0019FFD0` clears both tables, enables the letters `g`, `m`, `n` and `s`, and stores 144 paths of the
form `PS2Data\effect_finish\jp\chara\hNNNN.efx`.

### Shutting down

`001A0960` clears the run byte, waits for the thread to end (`005CD330`), frees the queue's nodes
(`002218D0`), marks it empty, drops pending completions, and closes the three locks' events
(`005CD6D0`). The destructor `0019F930` calls it and
then frees the pool, the completion vector and any list nodes left.

## Layouts

### Manager

`0x140228` bytes at `[01F81160]`.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `000` | `void*` | vtable | `AsyncLoadManager` |
| `008` | `Thread` | thread | the thread record of [runtime services](../Compiler-And-C-Runtime/runtime-services.md) (handle, start, argument; zeroed by `005CC900`), started by `001A0AF0` |
| `020` | `u8` | started | |
| `028` | `PhyreLock` | queue lock | the PhyreEngine lock of [runtime services](../Compiler-And-C-Runtime/runtime-services.md), built by `005CC8A0` |
| `050` | `List` | queue | an EASTL list: the anchor's next and previous (the tail) at `50` and `58`, its allocator at `60` named `EASTL list`; `0x18`-byte nodes, the record at node `10` |
| `068` | `u8` | queue empty | |
| `069` | `u8` | thread idle | |
| `070` | `PhyreLock` | completion lock | the PhyreEngine lock, built by `005CC8A0` |
| `098` | `Vector` | completions | an [EASTL vector](../Third-Party-Libraries/eastl-strings-and-containers.md): begin, end at `A0`, capacity at `A8`, allocator at `B0`; completion entries |
| `0B8` | `RecordPool` | requests | the pool template of [game application](../Engine-Core/game-application.md) (`0019F490`): vector at `+0`, sets at `+0x20` and `+0x58`, lock at `+0x90`, flag `+0xB8` 0 here; 1,024 request records |
| `178` | `PhyreLock` | pool lock | the PhyreEngine lock, built by `005CC8A0` |
| `1A0` | `u8` | run | |
| `1A1` | `u8[128]` | letter enable | indexed by the character code |
| `228` | `char*[163840]` | appendix paths | `[character × 1280 + number]`, the `.efx` path or null |

### Request record

`0x140` bytes.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `000` | `u32` | kind | `1` asset, `2` read by name, `3` read from a stream, `4` whole text |
| `008` | `void*` | callback | |
| `010` | `u64` | argument | kinds 2 and 3: replaced by the byte count |
| `018` | `u8` | complete on thread | `1` = call on the loading thread, `0` = next pump |
| `020` | `char[256]` | path | |
| `120` | `void*` | result | kinds 1 and 4: where to store; kinds 2 and 3: the destination |
| `128` | `u64` | second | kind 1: done byte pointer; kinds 2 and 3: file offset; kind 4: end pointer |
| `130` | `u32` | byte count | kinds 2 and 3; `FFFFFFFF` = the whole file |
| `138` | `void*` | stream | kind 3 |

### Completion entry

`0x18` bytes.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `void*` | callback | |
| `08` | `u64` | argument | |
| `10` | `u64` | on thread | the record's byte `18` |

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

The manager at `01F81160` with its queue, completion vector, record pool, the run, idle and empty
bytes, and the appendix tables, which nothing but `0019FFD0` writes. The read status `0215EFF4` and
its pointer `01F82CC0` for PS2 file reads.

## Modding notes

- At most 1,024 requests can be outstanding; with none free, `001BA860` returns 0 and every caller
  writes the kind through it without a test.
- The appendix is fixed in the executable: a model listed there always gets its effect file appended,
  so its size table entry must cover the model, the effect and 4 bytes. A model not listed gets
  nothing appended.
- Replacing an appended `.efx` changes the total; update that model's size in every `.fst`.
- A callback on a queued request with byte `+0x18` clear runs in the next frame, not when the file
  arrives.

## Related

- [File requests and the read queue](file-requests-and-the-read-queue.md): the PS2 request slots whose reads come here.
- [File size tables](file-size-tables-fst.md): the sizes the PS2 reads ask for.
- [Texture animation lists](texture-animation-lists-ta.md): one of the text lists read as kind 4.
- [Fonts](../Menus-And-HUD/fonts.md): the font lists and files read through this queue.
- [PhyreEngine asset files](../PhyreEngine/phyre-asset-files.md): what a kind 1 load does with the file.
- [Model files](../Graphics/model-files-cm-ca.md): the `.cm` files the appendix extends.
- [Effect files](../Graphics/effect-files-efx-efb.md): the `.efx` files it appends.
