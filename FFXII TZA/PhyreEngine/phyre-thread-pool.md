---
title: "Phyre thread pool: the PThreadPool the engine starts, its work-stealing worker threads and the job batches nothing submits"
kind: "system"
category: "PhyreEngine"
addresses: "006AA280, 006AA180, 006AA3A0, 006AA1B0, 006AA600, 006AA200, 006BA880, 006BAB40, 006BAED0, 006BB110, 006BB000, 006BAAD0, 006BADF0, 006BB070, 006BB0A0, 006BA940, 006CE5B0, 00D81200, 00D7C860, 00D8A730, 02E4E610, 02E5C938, 01F2EB30"
---

## What the player sees

Nothing. On a machine with more than one processor the engine starts one `PhyreEngineWorkerThread`
per processor when the game launches and stops them when it exits. No code in the game hands them
work, so they wait on a semaphore for the whole session and cost only their memory: 32 KiB of stack
and 256 KiB of scratch each.

## How it works

### Which pool

`006AA280` returns the engine's one `PThreadPool`, kept in `02E4E600` once chosen:

- with a worker count (`01F2EB30`) below 2, the `PThreadPoolImmediate` static `02E5C938`
  (`006CE5B0`, vtable `00D8A730`, exit destructor `008B70D0`);
- otherwise the `PThreadPoolWorkStealing` static `02E4E610`, built on first use by
  `006BA880(pool, workers, capacity)` with `01F2EB30` and `01F2EB3C`, and destroyed at exit by
  `008B41F0` through `006BA940`.

`01F2EB30` is 1 in the image. The start-up's `007979B0` counts the bits of the process affinity mask
(or takes `GetSystemInfo`'s processor count when that is 0) and stores the count through `006AA370`
when it is above 1.

### Start and stop

The engine start-up `005A08E0` stores the scratch size `40000`<sub>h</sub> (`01F2EB34`), the stack size `8000`<sub>h</sub>
(`01F2EB38`) and the job capacity `800`<sub>h</sub> (`01F2EB3C`), then calls slot 2 of the pool; a non-zero
result ends the start-up. The engine shutdown `005A0840` calls slot 3. `006AA280` has no other caller, and no instruction outside it
reads `02E4E600`, `02E4E610` or `02E5C930`, so nothing else reaches the pool.

### The base class

`006AA180(pool, workers, capacity)` writes the `PThreadPool` vtable `00D7C860`, the worker count at
`+10`<sub>h</sub> and the capacity at `+24`<sub>h</sub>, and zeroes the rest. Every slot of that vtable except slot 1
(`006AA230`, the deleting destructor) is `_purecall`.

`006AA3A0(pool, scratchSize, stackSize)` starts the workers:

1. It allocates the worker array, `38`<sub>h</sub> bytes per worker behind a count, each entry constructed by
   `006AA1B0`, which zeroes the pool pointer, scratch pointer, thread record, started byte, index
   word and stop byte.
2. It allocates job list A (`+28`<sub>h</sub>, capacity × 8 bytes, zeroed) and one scratch block of
   `scratchSize` × workers aligned to `80`<sub>h</sub> (`+18`<sub>h</sub>), and stores `scratchSize` at `+20`<sub>h</sub>.
3. For each worker it fills the entry (pool, its slice of the scratch block, index, worker count) and
   creates a thread (`005CD1E0`) named `PhyreEngineWorkerThread%d`, with `stackSize` bytes of stack,
   below-normal priority (mode 2) and entry `006AA390`, which jumps to slot 0 of the pool with the
   entry.

Allocation failures return `D`<sub>h</sub>; a failed thread start returns its error. The affinity mask it
computes from `02E4E5F0` is passed to `0016D6A0`, which only returns, so every worker may run on any
processor.

`006AA600(pool)` is the base teardown: it waits for each worker's thread to end (`005CD330`), clears
its started byte, frees the worker array, job list A and the scratch block, and nulls their
pointers. The base destructors `006AA200` and `006AA230` write the base vtable and call it.

### The work-stealing pool

`006BA880` adds the vtable `00D81200`, two pairs of semaphore records and the generation fields to the
base, with both "waited" bytes at `+90`<sub>h</sub> set. Its slots:

| Slot | Function | What it does |
|---|---|---|
| 0 | `006BB110` | the worker loop |
| 1 | `006BAA40` | deleting destructor (`006BA940` without the free) |
| 2 | `006BAB40` | start |
| 3 | `006BAED0` | stop |
| 4 | `006BB000` | add a job; `E`<sub>h</sub> when the list is full |
| 5 | `006BAAD0` | add a job; kicks the batch when the list becomes full |
| 6 | `006BADF0` | kick the pending batch |
| 7 | `006BB070` | wait for a job's batch |

`006BAB40` returns 7 when the worker count or the capacity is 0. It gives each worker a
`PProcessorProfileTimelineCpu` object (array at `+30`<sub>h</sub>; the naming and registration calls on it are
the stub `005C5230`), allocates the two range arrays (`+98`<sub>h</sub>, `+A0`<sub>h</sub>, `18`<sub>h</sub> bytes per worker),
creates the start semaphores `+38`<sub>h</sub> and `+48`<sub>h</sub> and the done semaphores `+58`<sub>h</sub> and `+68`<sub>h</sub>
(`005CD160`, count 0, maximum the worker count), allocates job list B (`+80`<sub>h</sub>), and ends with
`006AA3A0`.

### Batches

Jobs go into one of two lists by the parity of the generation word `+78`<sub>h</sub>: list A for even, B for
odd. A job is an object whose `+10`<sub>h</sub> receives the generation it was added in.

1. Adding (`006BB000`, `006BAAD0`) first calls `006BB0A0(pool, generation − 2)`, so a list is reused
   only after the batch that last used it has finished, then appends the job and counts it at
   `+88`<sub>h</sub>.
2. Kicking (`006BADF0`) does nothing with no pending jobs. Otherwise it records the generation
   (`+7C`<sub>h</sub>) and job count (`+8C`<sub>h</sub>), clears the waited byte of parity *b*, advances the generation,
   splits the list evenly between the workers, worker *i* getting entries `n·i/w` to `n·(i+1)/w` as a
   cursor and end in range array *b*, and releases start semaphore *b* once per worker.
3. Waiting (`006BB070`) kicks first when the job's generation is still the current one, then calls
   `006BB0A0`.

`006BB0A0(pool, generation)` acts only when the generation is less than three behind the current one
and its parity's waited byte is clear: it waits on done semaphore *b* once per worker and sets the
byte.

### The worker loop

`006BB110(pool, worker)` alternates between parities 0 and 1:

1. It waits on start semaphore *b*; with the worker's stop byte (`+34`<sub>h</sub>) set it returns 0.
2. It visits every worker's range, starting with its own (index `(k + own) mod w`), and claims entries
   by advancing the range's cursor with a 32-bit interlocked compare-exchange on its low half while the
   cursor is below the end. A null entry ends that range.
3. For each claimed job it calls the job's slot 1 with its scratch slice, the scratch size and its own
   index.
4. It releases done semaphore *b* once.

### Stopping

`006BAED0` frees the profile objects, sets every worker's stop byte and releases the start semaphore
of the current parity once per worker, so each worker wakes and returns. `006AA600` then joins the
threads, and `006BAED0` closes the four semaphores and frees job list B and the range arrays.

### The immediate pool

`PThreadPoolImmediate` runs a job at once on the calling thread:

| Slot | Function | What it does |
|---|---|---|
| 0 | `005C5230` | returns 0 |
| 1 | `006CE570` | deleting destructor |
| 2 | `006CE670` | allocates one scratch block of `01F2EB34` bytes at `+18`<sub>h</sub>; `D`<sub>h</sub> on failure |
| 3 | `006CE6C0` | frees it |
| 4, 5 | `006CE6E0`, `006CE650` | call the job's slot 1 with the scratch block, its size and worker 0 |
| 6, 7 | `0016D6A0` | return |

## Layouts

`PThreadPoolWorkStealing` (`A8`<sub>h</sub> bytes, offsets from the start of the 02E4E610):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `void*` | vtable | `00D81200` |
| `08`<sub>h</sub> | `void*` | workers | `38`<sub>h</sub>-byte entries |
| `10`<sub>h</sub> | `u32` | workerCount |  |
| `18`<sub>h</sub> | `void*` | scratch | workerCount x scratchSize, `80`<sub>h</sub>-aligned |
| `20`<sub>h</sub> | `u32` | scratchSize |  |
| `24`<sub>h</sub> | `u32` | capacity | jobs per list |
| `28`<sub>h</sub> | `void*` | listA | even generations |
| `30`<sub>h</sub> | `void*` | profiles | one PProcessorProfileTimelineCpu per worker |
| `38`<sub>h</sub> | `u8[16]` | start0 | semaphore record: handle, then created byte at +`08`<sub>h</sub> |
| `48`<sub>h</sub> | `u8[16]` | start1 |  |
| `58`<sub>h</sub> | `u8[16]` | done0 |  |
| `68`<sub>h</sub> | `u8[16]` | done1 |  |
| `78`<sub>h</sub> | `u32` | generation |  |
| `7C`<sub>h</sub> | `u32` | kickedGeneration |  |
| `80`<sub>h</sub> | `void*` | listB | odd generations |
| `88`<sub>h</sub> | `u32` | pending | jobs added since the last kick |
| `8C`<sub>h</sub> | `u32` | kicked | jobs in the last kick |
| `90`<sub>h</sub> | `u8[2]` | waited | per parity |
| `98`<sub>h</sub> | `void*` | ranges0 | `18`<sub>h</sub> bytes per worker |
| `A0`<sub>h</sub> | `void*` | ranges1 |  |

`PThreadPoolWorker` (`38`<sub>h</sub> bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `void*` | pool |  |
| `08`<sub>h</sub> | `void*` | scratch | this worker's slice |
| `10`<sub>h</sub> | `u8[24]` | thread | handle, entry, argument |
| `28`<sub>h</sub> | `u8` | started |  |
| `30`<sub>h</sub> | `u16` | index |  |
| `32`<sub>h</sub> | `u16` | workerCount |  |
| `34`<sub>h</sub> | `u8` | stop |  |

`ThreadPoolRange` (`18`<sub>h</sub> bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `void*` | profile | the worker's profile object |
| `08`<sub>h</sub> | `void*` | cursor | next job pointer to claim |
| `10`<sub>h</sub> | `void*` | end |  |

## State

| Address | What |
|---|---|
| `02E4E600` | the chosen pool |
| `02E4E610` | the `PThreadPoolWorkStealing` static (guard `02E4E6B8`) |
| `02E5C930`, `02E5C938` | the chosen immediate pool and its static (guard `02E5C968`) |
| `01F2EB30` | worker count; 1 in the image |
| `01F2EB34`, `01F2EB38`, `01F2EB3C` | scratch size, stack size, job capacity |

## Modding notes

- The worker threads exist but receive no work. A mod can hand them jobs through slots 4 to 7 of the
  pool `006AA280` returns; a job needs a vtable whose slot 1 takes `(job, scratch, scratchSize,
  workerIndex)`.
- A job's slot 1 runs on any worker, and a worker may run jobs from every other worker's share.
- The cursor is claimed with a 32-bit compare-exchange, so a job list must not cross a 4 GiB address
  boundary.
- On a single-processor machine the immediate pool runs each job inside the add call.

## Related

- [Class hierarchy](../Engine-Core/class-hierarchy.md): the RTTI the class names come from.
- [Memory and allocation](../Compiler-And-C-Runtime/memory-and-allocation.md): the heap the scratch blocks and job lists come from.
