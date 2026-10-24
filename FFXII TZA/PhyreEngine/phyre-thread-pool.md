---
title: "Phyre thread pool: the PThreadPool the engine starts, its work-stealing worker threads and the job batches nothing submits"
kind: "system"
category: "PhyreEngine"
addresses: "0x006AA280, 0x006AA180, 0x006AA3A0, 0x006AA1B0, 0x006AA600, 0x006AA200, 0x006BA880, 0x006BAB40, 0x006BAED0, 0x006BB110, 0x006BB000, 0x006BAAD0, 0x006BADF0, 0x006BB070, 0x006BB0A0, 0x006BA940, 0x006CE5B0, 0x00D81200, 0x00D7C860, 0x00D8A730, 0x02E4E610, 0x02E5C938, 0x01F2EB30"
---

## What the player sees

Nothing. On a machine with more than one processor the engine starts one `PhyreEngineWorkerThread`
per processor when the game launches and stops them when it exits. No code in the game hands them
work, so they wait on a semaphore for the whole session and cost only their memory: 32 KiB of stack
and 256 KiB of scratch each.

## How it works

### Which pool

`0x006AA280` returns the engine's one `PThreadPool`, kept in `0x02E4E600` once chosen:

- with a worker count (`0x01F2EB30`) below 2, the `PThreadPoolImmediate` static `0x02E5C938`
  (`0x006CE5B0`, vtable `0x00D8A730`, exit destructor `0x008B70D0`);
- otherwise the `PThreadPoolWorkStealing` static `0x02E4E610`, built on first use by
  `0x006BA880(pool, workers, capacity)` with `0x01F2EB30` and `0x01F2EB3C`, and destroyed at exit by
  `0x008B41F0` through `0x006BA940`.

`0x01F2EB30` is 1 in the image. The start-up's `0x007979B0` counts the bits of the process affinity mask
(or takes `GetSystemInfo`'s processor count when that is 0) and stores the count through `0x006AA370`
when it is above 1.

### Start and stop

The engine start-up `0x005A08E0` stores the scratch size `0x40000` (`0x01F2EB34`), the stack size `0x8000`
(`0x01F2EB38`) and the job capacity `0x800` (`0x01F2EB3C`), then calls slot 2 of the pool; a non-zero
result ends the start-up. The engine shutdown `0x005A0840` calls slot 3. `0x006AA280` has no other caller, and no instruction outside it
reads `0x02E4E600`, `0x02E4E610` or `0x02E5C930`, so nothing else reaches the pool.

### The base class

`0x006AA180(pool, workers, capacity)` writes the `PThreadPool` vtable `0x00D7C860`, the worker count at
`+0x10` and the capacity at `+0x24`, and zeroes the rest. Every slot of that vtable except slot 1
(`0x006AA230`, the deleting destructor) is `_purecall`.

`0x006AA3A0(pool, scratchSize, stackSize)` starts the workers:

1. It allocates the worker array, `0x38` bytes per worker behind a count, each entry constructed by
   `0x006AA1B0`, which zeroes the pool pointer, scratch pointer, thread record, started byte, index
   word and stop byte.
2. It allocates job list A (`+0x28`, capacity × 8 bytes, zeroed) and one scratch block of
   `scratchSize` × workers aligned to `0x80` (`+0x18`), and stores `scratchSize` at `+0x20`.
3. For each worker it fills the entry (pool, its slice of the scratch block, index, worker count) and
   creates a thread (`0x005CD1E0`) named `PhyreEngineWorkerThread%d`, with `stackSize` bytes of stack,
   below-normal priority (mode 2) and entry `0x006AA390`, which jumps to slot 0 of the pool with the
   entry.

Allocation failures return `0xD`; a failed thread start returns its error. The affinity mask it
computes from `0x02E4E5F0` is passed to `0x0016D6A0`, which only returns, so every worker may run on any
processor.

`0x006AA600(pool)` is the base teardown: it waits for each worker's thread to end (`0x005CD330`), clears
its started byte, frees the worker array, job list A and the scratch block, and nulls their
pointers. The base destructors `0x006AA200` and `0x006AA230` write the base vtable and call it.

### The work-stealing pool

`0x006BA880` adds the vtable `0x00D81200`, two pairs of semaphore records and the generation fields to the
base, with both "waited" bytes at `+0x90` set. Its slots:

| Slot | Function | What it does |
|---|---|---|
| 0 | `0x006BB110` | the worker loop |
| 1 | `0x006BAA40` | deleting destructor (`0x006BA940` without the free) |
| 2 | `0x006BAB40` | start |
| 3 | `0x006BAED0` | stop |
| 4 | `0x006BB000` | add a job; `0xE` when the list is full |
| 5 | `0x006BAAD0` | add a job; kicks the batch when the list becomes full |
| 6 | `0x006BADF0` | kick the pending batch |
| 7 | `0x006BB070` | wait for a job's batch |

`0x006BAB40` returns 7 when the worker count or the capacity is 0. It gives each worker a
`PProcessorProfileTimelineCpu` object (array at `+0x30`; the naming and registration calls on it are
the stub `0x005C5230`), allocates the two range arrays (`+0x98`, `+0xA0`, `0x18` bytes per worker),
creates the start semaphores `+0x38` and `+0x48` and the done semaphores `+0x58` and `+0x68`
(`0x005CD160`, count 0, maximum the worker count), allocates job list B (`+0x80`), and ends with
`0x006AA3A0`.

### Batches

Jobs go into one of two lists by the parity of the generation word `+0x78`: list A for even, B for
odd. A job is an object whose `+0x10` receives the generation it was added in.

1. Adding (`0x006BB000`, `0x006BAAD0`) first calls `0x006BB0A0(pool, generation − 2)`, so a list is reused
   only after the batch that last used it has finished, then appends the job and counts it at
   `+0x88`.
2. Kicking (`0x006BADF0`) does nothing with no pending jobs. Otherwise it records the generation
   (`+0x7C`) and job count (`+0x8C`), clears the waited byte of parity *b*, advances the generation,
   splits the list evenly between the workers, worker *i* getting entries `n·i/w` to `n·(i+1)/w` as a
   cursor and end in range array *b*, and releases start semaphore *b* once per worker.
3. Waiting (`0x006BB070`) kicks first when the job's generation is still the current one, then calls
   `0x006BB0A0`.

`0x006BB0A0(pool, generation)` acts only when the generation is less than three behind the current one
and its parity's waited byte is clear: it waits on done semaphore *b* once per worker and sets the
byte.

### The worker loop

`0x006BB110(pool, worker)` alternates between parities 0 and 1:

1. It waits on start semaphore *b*; with the worker's stop byte (`+0x34`) set it returns 0.
2. It visits every worker's range, starting with its own (index `(k + own) mod w`), and claims entries
   by advancing the range's cursor with a 32-bit interlocked compare-exchange on its low half while the
   cursor is below the end. A null entry ends that range.
3. For each claimed job it calls the job's slot 1 with its scratch slice, the scratch size and its own
   index.
4. It releases done semaphore *b* once.

### Stopping

`0x006BAED0` frees the profile objects, sets every worker's stop byte and releases the start semaphore
of the current parity once per worker, so each worker wakes and returns. `0x006AA600` then joins the
threads, and `0x006BAED0` closes the four semaphores and frees job list B and the range arrays.

### The immediate pool

`PThreadPoolImmediate` runs a job at once on the calling thread:

| Slot | Function | What it does |
|---|---|---|
| 0 | `0x005C5230` | returns 0 |
| 1 | `0x006CE570` | deleting destructor |
| 2 | `0x006CE670` | allocates one scratch block of `0x01F2EB34` bytes at `+0x18`; `0xD` on failure |
| 3 | `0x006CE6C0` | frees it |
| 4, 5 | `0x006CE6E0`, `0x006CE650` | call the job's slot 1 with the scratch block, its size and worker 0 |
| 6, 7 | `0x0016D6A0` | return |

## Layouts

`PThreadPoolWorkStealing` (`0xA8` bytes, offsets from the start of the 0x02E4E610):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | vtable | `0x00D81200` |
| `+0x08` | `void*` | workers | `0x38`-byte entries |
| `+0x10` | `u32` | workerCount |  |
| `+0x18` | `void*` | scratch | workerCount x scratchSize, `0x80`-aligned |
| `+0x20` | `u32` | scratchSize |  |
| `+0x24` | `u32` | capacity | jobs per list |
| `+0x28` | `void*` | listA | even generations |
| `+0x30` | `void*` | profiles | one PProcessorProfileTimelineCpu per worker |
| `+0x38` | `u8[16]` | start0 | semaphore record: handle, then created byte at `+0x08` |
| `+0x48` | `u8[16]` | start1 |  |
| `+0x58` | `u8[16]` | done0 |  |
| `+0x68` | `u8[16]` | done1 |  |
| `+0x78` | `u32` | generation |  |
| `+0x7C` | `u32` | kickedGeneration |  |
| `+0x80` | `void*` | listB | odd generations |
| `+0x88` | `u32` | pending | jobs added since the last kick |
| `+0x8C` | `u32` | kicked | jobs in the last kick |
| `+0x90` | `u8[2]` | waited | per parity |
| `+0x98` | `void*` | ranges0 | `0x18` bytes per worker |
| `+0xA0` | `void*` | ranges1 |  |

`PThreadPoolWorker` (`0x38` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | pool |  |
| `+0x08` | `void*` | scratch | this worker's slice |
| `+0x10` | `u8[24]` | thread | handle, entry, argument |
| `+0x28` | `u8` | started |  |
| `+0x30` | `u16` | index |  |
| `+0x32` | `u16` | workerCount |  |
| `+0x34` | `u8` | stop |  |

`ThreadPoolRange` (`0x18` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | profile | the worker's profile object |
| `+0x08` | `void*` | cursor | next job pointer to claim |
| `+0x10` | `void*` | end |  |

## State

| Address | What |
|---|---|
| `0x02E4E600` | the chosen pool |
| `0x02E4E610` | the `PThreadPoolWorkStealing` static (guard `0x02E4E6B8`) |
| `0x02E5C930`, `0x02E5C938` | the chosen immediate pool and its static (guard `0x02E5C968`) |
| `0x01F2EB30` | worker count; 1 in the image |
| `0x01F2EB34`, `0x01F2EB38`, `0x01F2EB3C` | scratch size, stack size, job capacity |

## Modding notes

- The worker threads exist but receive no work. A mod can hand them jobs through slots 4 to 7 of the
  pool `0x006AA280` returns; a job needs a vtable whose slot 1 takes `(job, scratch, scratchSize,
  workerIndex)`.
- A job's slot 1 runs on any worker, and a worker may run jobs from every other worker's share.
- The cursor is claimed with a 32-bit compare-exchange, so a job list must not cross a 4 GiB address
  boundary.
- On a single-processor machine the immediate pool runs each job inside the add call.

## Related

- [Class hierarchy](../Engine-Core/class-hierarchy.md): the RTTI the class names come from.
- [Memory and allocation](../Compiler-And-C-Runtime/memory-and-allocation.md): the heap the scratch blocks and job lists come from.
