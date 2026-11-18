[Home](../../README.md) / [PhyreEngine](README.md) / Phyre thread pool

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Phyre thread pool: the PThreadPool the engine starts, its work-stealing worker threads and the job batches nothing submits | system | PhyreEngine | Engine framework | PhyreEngine's PThreadPool as the executable carries it: the choice between the work-stealing pool and the immediate pool by processor count, the start and stop the module walk runs, the PhyreEngineWorkerThread threads with their scratch memory, the double-buffered job lists split between workers and stolen through a shared cursor, the add, kick and wait slots, and the fact that no code ever submits a job, so the workers sleep for the whole session. | 0x006AA280, 0x006AA180, 0x006AA3A0, 0x006AA1B0, 0x006AA600, 0x006AA200, 0x006BA880, 0x006BAB40, 0x006BAED0, 0x006BB110, 0x006BB000, 0x006BAAD0, 0x006BADF0, 0x006BB070, 0x006BB0A0, 0x006BA940, 0x006CE5B0, 0x00D81200, 0x00D7C860, 0x00D8A730, 0x02E4E610, 0x02E5C938, 0x01F2EB30 |

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
  `0x006BA880(pool, workers, capacity)` with `0x01F2EB30` and `0x01F2EB3C`, and destroyed by `0x008B41F0` through
  `0x006BA940` only when the run-time `exit` runs the teardowns; the normal quit ends in `ExitProcess(0)` before that.
- `0x006CE5B0` returns the pool held in `0x02E5C930` when that is set (`0x006CE5C9`), else builds the static once under
  the guard `0x02E5C968` with `0x006AA180(pool, 0, 0)`, so its worker count and capacity are 0 (`0x006CE614`), writes
  the vtable (`0x006CE620`), stores the static in `0x02E5C930` (`0x006CE640`) and returns it.
- `0x006BA940` writes the vtable `0x00D81200`, runs the stop `0x006BAED0` (`0x006BA95C`), destroys the two
  semaphore record pairs with the `ret 0` stub `0x0016D6A0` as each record's destructor (`0x006BA976`, `0x006BA990`) and
  tail-jumps to the base destructor `0x006AA200` (`0x006BA99E`), which writes `0x00D7C860` and calls `0x006AA600`.

`0x01F2EB30` is 1 in the image. The start-up's `0x007979B0` counts the bits of the process affinity mask
(or takes `GetSystemInfo`'s processor count when that is 0) and stores the count through `0x006AA370`
when it is above 1.

### Start and stop

The engine start-up `0x005A08E0` stores the scratch size `0x40000` (`0x01F2EB34`), the stack size `0x8000`
(`0x01F2EB38`) and the job capacity `0x800` (`0x01F2EB3C`), then calls slot 2 of the pool; a non-zero
result ends the start-up. The engine shutdown `0x005A0840` calls slot 3.

`0x006AA280` has no other caller (`0x005A0877`, `0x005A0A8E`), and only it names `0x02E4E600` (`0x006AA28F`, `0x006AA2AD`,
`0x006AA325`). Besides `0x006AA280` (`0x006AA2CF`), `0x02E4E610` is named only by the exit destructor `0x008B41F0`, which
passes it to `0x006BA940`. `0x02E5C930` is named only by `0x006CE5B0` (`0x006CE5BF`, `0x006CE640`), whose one caller is
`0x006AA280` (`0x006AA2A8`). No image word points at any of the three, so nothing else reaches the pool.

### The base class

`0x006AA180(pool, workers, capacity)` writes the `PThreadPool` vtable `0x00D7C860`, the worker count at
`+0x10` and the capacity at `+0x24`, and zeroes the rest. Every slot of that vtable except slot 1
(`0x006AA230`, the deleting destructor) is `_purecall`.

`0x006AA3A0(pool, scratchSize, stackSize)` starts the workers:

1. It allocates the worker array, `0x38` bytes per worker behind a count, each entry constructed by
   `0x006AA1B0`, which zeroes the pool pointer, scratch pointer, thread record, started byte, index
   word and stop byte. A worker count of 0 skips the array (`0x006AA3F9`).
2. `0x006AA1B0` zeroes the thread record's three quadwords through `0x005CC900` (`0x006AA1CF`). Its 32-bit store at
   `+0x30` (`0x006AA1E0`) also zeroes the worker-count word `+0x32`, and it returns the entry.
3. It allocates job list A (`+0x28`, capacity × 8 bytes, zeroed) and one scratch block of
   `scratchSize` × workers aligned to `0x80` (`+0x18`), and stores `scratchSize` at `+0x20`.
   A capacity of 0 skips list A (`0x006AA46B`) and a `scratchSize` of 0 skips the scratch block (`0x006AA4A4`);
   the store at `+0x20` is made either way (`0x006AA4C0`).
4. For each worker it fills the entry (pool, its slice of the scratch block, index, worker count) and
   creates a thread (`0x005CD1E0`) named `PhyreEngineWorkerThread%d`, with `stackSize` bytes of stack,
   below-normal priority (mode 2) and entry `0x006AA390`, which jumps to slot 0 of the pool with the
   entry.
5. Worker `i` gets the slice `scratch + i * scratchSize` (`0x006AA4F6`, `0x006AA5BF`), its index in the word `+0x30`
   and the worker count's low 16 bits in `+0x32` (`0x006AA4FB`, `0x006AA505`). Its started byte is set to 1 right
   after the create call, before the result is tested (`0x006AA5B2`, `0x006AA5B8`).

Allocation failures return `0xD` (`0x006AA459`); a failed thread start returns its error and leaves the later
workers unstarted (`0x006AA5BA`); with every thread started it returns 0 (`0x006AA5CF`). The affinity mask it
computes from `0x02E4E5F0` is passed to `0x0016D6A0`, which only returns, so every worker may run on any
processor.

The mask is built when the running mask is 0 (`0x006AA559`): for the first worker, and again once the
one-bit-per-worker mode has handed out every bit. It is `[0x02E4E5F0]` through `0x0016D680`, which returns its
argument, or all bits when that is 0 (`0x006AA572`), and `and rbx, 0xfffffffffffffffc` clears its bits `0x1` and
`0x2` (`0x006AA57E`). When the dword `0x02E4E5F8` is 1, each worker takes the lowest set bit,
`bit = m - (m & (m - 1))`, and keeps `m & (m - 1)` for the next worker (`0x006AA58E`-`0x006AA598`); otherwise each
worker takes the whole mask.

The thread parameters keep the all-processors mask `-1` that `0x005CC8C0` writes at their `+0x30` (`0x005CC8EE`),
and `0x005CD1E0` hands that value to `SetThreadAffinityMask` (`0x005CD28B`).

`0x006AA600(pool)` is the base teardown: it waits for each worker's thread to end (`0x005CD330`), clears
its started byte, frees the worker array, job list A and the scratch block, and nulls their
pointers. The base destructors `0x006AA200` and `0x006AA230` write the base vtable and call it.

With a null worker array `0x006AA600` skips the per-worker loop and the array's free (`0x006AA627`, `0x006AA667`).
For each worker it calls `0x005CD330`, which waits on the thread handle without a timeout and copies the exit code
into a local of `0x006AA600` that nothing reads (`0x005CD346`, `0x005CD354`), then the stub `0x005C5230` on the thread
record (`0x006AA650`), and clears the started byte whatever the wait found (`0x006AA655`).

The array goes through the vector destructor iterator `0x00809054` with the `ret 0` stub `0x0016D6A0` as each entry's
destructor (`0x006AA67C`) and is freed from its count header (`0x006AA685`). Job list A and the scratch block are
freed through `0x00584730`, which skips a null pointer (`0x00584733`), at `0x006AA68F` and `0x006AA698`; the three
pointers are nulled at `0x006AA69D`-`0x006AA6A5`.

### The work-stealing pool

`0x006BA880` adds the vtable `0x00D81200`, two pairs of semaphore records and the generation fields to the
base, with both "waited" bytes at `+0x90` set. It first runs `0x006AA180` with its own worker count and capacity
(`0x006BA8A0`) and builds the records at `+0x38` and `+0x58` with `0x005DBF90`, which clears each record's created
byte (`0x006BA8D4`, `0x006BA8F1`, `0x005DBFA1`).

It zeroes the profile pointer `+0x30`, both generation words, list B, the counts `+0x88` and `+0x8C` and both
range pointers (`0x006BA8B2`, `0x006BA8F6`-`0x006BA91F`), writes `0x101` to the waited bytes (`0x006BA90F`) and returns
the pool. Its slots:

| Slot | Function | What it does |
|---|---|---|
| 0 | `0x006BB110` | the worker loop |
| 1 | `0x006BAA40` | deleting destructor (`0x006BA940` without the free) |
| 2 | `0x006BAB40` | start |
| 3 | `0x006BAED0` | stop |
| 4 | `0x006BB000` | add a job; returns 0 (`0x006BB05E`), or `0xE` when the list is full (`pending >= capacity`, `0x006BB03D`), after it has already called `0x006BB0A0` and written the generation into the job's `+0x10` (`0x006BB016`, `0x006BB01E`) |
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
3. The kick zeroes the pending count `+0x88` as it advances the generation (`0x006BAE51`, `0x006BAE55`). Each end is
   `list + (n * (i + 1) / w) * 8`, with a 32-bit product and quotient (`0x006BAE89`, `0x006BAE8D`); each cursor is
   the previous worker's end, the first one the list itself (`0x006BAE77`). The release is one `ReleaseSemaphore`
   call with a count of `w` (`0x006BAEB1`, `0x005CD661`).
4. Waiting (`0x006BB070`) kicks first when the job's generation is still the current one, then calls
   `0x006BB0A0`.

`0x006BB0A0(pool, generation)` acts only when the generation is less than three behind the current one
and its parity's waited byte is clear: it waits on done semaphore *b* once per worker and sets the
byte.

### The worker loop

Before its loop, `0x006BB110` reads its index, scratch slice and `w` from its own entry (`+0x30`, `+0x08`, `+0x32`) and
the scratch size from the pool's `+0x20` (`0x006BB139`-`0x006BB152`). It formats `WorkerThread:%d` with its index
into a 256-byte local buffer that nothing reads afterwards (`0x006BB16E`). Range array *b* is `+0x98` for
parity 0 and `+0xA0` for parity 1 (`0x006BB1BC`, `0x006BB266`).

`0x006BB110(pool, worker)` alternates between parities 0 and 1:

1. It waits on start semaphore *b*; with the worker's stop byte (`+0x34`) set it returns 0.
2. It visits every worker's range, starting with its own (index `(k + own) mod w`), and claims entries
   by advancing the range's cursor with a 32-bit interlocked compare-exchange on its low half while the
   cursor is below the end. A null entry ends that range. A failed exchange rereads the cursor and retries
   while it is below the end (`0x006BB220`-`0x006BB23B`).
3. For each claimed job it calls the job's slot 1 with its scratch slice, the scratch size and its own
   index. After the job returns it goes back to the same range (`0x006BB2E9`).
4. It releases done semaphore *b* once (count 1, `0x006BB25C`); with `w` 0 it visits no range and goes straight
   to this release (`0x006BB1C9`).
5. After parity 1's release it tests the stop byte again, so a worker stopped by then returns 0 without
   waiting again (`0x006BB28A`-`0x006BB297`); otherwise it starts over at parity 0.

### Stopping

`0x006BAED0` frees the profile objects, sets every worker's stop byte and releases the start semaphore
of the current parity once per worker, so each worker wakes and returns. `0x006AA600` then joins the
threads, and `0x006BAED0` closes the four semaphores and frees job list B and the range arrays.

Before the free it calls the stub `0x005C5230` with `0x01F2ED08` and each worker's profile slot (`0x006BAEFF`). A
non-empty profile array goes to the first object's slot 0 with flag 3, the vector deleting destructor
(`0x006BAF23`); an empty one is freed from its header by `0x00210EB0` (`0x006BAF2B`); `+0x30` is nulled either way
(`0x006BAF30`).

The stop bytes, the release, the closing and the frees run only when the range block `+0x98` that `0x006BAB40`
allocates is set (`0x006BAF42`, `0x006BAF8D`); `0x006AA600` runs in both cases (`0x006BAF85`). Closing clears each
record's created byte (`0x006BAF9C`-`0x006BAFBF`). The two range arrays are one block (`0x006BAC76`, `0x006BAC9E`), so
freeing `+0x98` frees both; `+0x80` and `+0x98` are nulled and `+0xA0` keeps its old pointer (`0x006BAFDB`,
`0x006BAFE6`).

The exit destructor `0x006BA940` runs only when the run-time `exit` runs the teardowns; the normal quit ends in
`ExitProcess(0)` before that
([static initialisation and teardown](../Compiler-And-C-Runtime/static-initialisation-and-teardown.md)).
When it runs after the shutdown's slot 3, it runs `0x006BAED0` a second time; with `+0x30`, `+0x98` and the worker array
already null, only the stub calls and `0x006AA600` run then, and `0x006AA600` finds every pointer null.

The destructor is
registered at the pool's first use (`0x006AA313`), which is `0x005A08E0`'s call at `0x005A0A8E`, before it sets its guard.
After a failure at `0x005A0A9E` or `0x005A0ABE` the shutdown therefore skips slot 3 (`0x005A084B`), and this call is the
pool's first stop. The four earlier failure exits (`0x005A0927`, `0x005A0A3E`, `0x005A0A54`, `0x005A0A61`) come before
`0x005A0A8E`, so no pool exists and no destructor is registered.

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

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Presentation: `0x0016D680` is called by `0x00183A00`, `0x00183C60`, `0x00183EE0`, `0x001946E0`, `0x003ED8A0`, `0x003EE2D0`; those
  functions are documented on [effect files efx efb](../Graphics/effect-files-efx-efb.md),
  [tim2 images](../Game-Files-And-Data-Tables/tim2-images.md),
  [random number generators](../Random-Numbers/random-number-generators.md).
- Presentation: and on [effect element runtime](../Graphics/effect-element-runtime.md).
