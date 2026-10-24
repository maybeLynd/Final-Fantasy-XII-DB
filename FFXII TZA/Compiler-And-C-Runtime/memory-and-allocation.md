---
title: "Memory and allocation: the C runtime heap, the game's allocation wrappers, new and delete, aligned blocks and the subsystem allocators"
kind: "system"
category: "Compiler and C runtime"
addresses: "0x008C2B40, 0x008C2B48, 0x008C2B60, 0x008C2B70, 0x008C2B78, 0x00210EC0, 0x00210EB0, 0x00809950, 0x0085E730, 0x0019C590, 0x0017D260, 0x00584740, 0x00584730, 0x0019C580, 0x0019C570, 0x002099D0, 0x001A5A80, 0x0016D6B0, 0x0016D6C0, 0x008F6500, 0x00902720, 0x001EDF00, 0x001EDF10, 0x001EDF80, 0x001EDFE0, 0x01F82E48, 0x00808D5C, 0x0036D240, 0x0036D250, 0x0020C610, 0x01F83448, 0x01F83440, 0x01F83441, 0x0020C6B0, 0x01F83438, 0x00792F10, 0x002679F0, 0x01E0C328, 0x00267930, 0x00267BB0, 0x00267C20, 0x006CC5A0, 0x01F2EAA8, 0x01F2EAB0, 0x01F2EA70, 0x00675460, 0x003E9AA0, 0x0025A990, 0x0025AA30, 0x0085E690"
---

## What the player sees

The game's memory use in Task Manager climbs as areas, models and movies load and falls as they are
released. About 257 MiB is taken in one go at start-up for the resource arenas. The RAM file cache
may grow to a third of the machine's physical memory, never below 32 MiB and never above 4 GiB, and
on start the game raises its own process priority and widens its working set to nearly all
physical memory.

## How it works

### One heap, reached through eight imports

All dynamic memory comes from the C runtime heap of `api-ms-win-crt-heap-l1-1-0.dll`. Its eight
imports sit in consecutive slots: `malloc` `0x008C2B40`, `free` `0x008C2B48`, `_msize` `0x008C2B50`,
`realloc` `0x008C2B58`, `_aligned_malloc` `0x008C2B60`, `calloc` `0x008C2B68`, `_aligned_free` `0x008C2B70`
and `_set_new_mode` `0x008C2B78`. The image imports no `VirtualAlloc`, `HeapAlloc`, `HeapCreate` or
`MapViewOfFile`, and no `operator new`, `operator delete` or `_callnewh` from `VCRUNTIME140.dll` or
`MSVCP140.dll`.

Every other memory system on this page, and the arenas on the
[resource arena page](../Game-Files-And-Data-Tables/resource-arena-and-relocation.md), sits on
top of these imports. The remaining allocating imports serve narrow jobs: `GlobalAlloc` has one call
(`0x00798DED`), filling a clipboard buffer before `SetClipboardData`; `LocalAlloc` has sixteen, in
`0x00159420` to `0x0015B6CD`, the first of which sizes a buffer for a `GetSystemDirectoryW` path.

The first entry of the C++ initialiser table (`0x008C31D8`) is `0x00808D5C`. It installs the unhandled
exception filter (`0x00809B44`) and then calls `_set_new_mode` through `0x00808D70` and the import stub
`0x00862046` with the result of `0x005C5230`, which is `xor eax, eax; ret`. The new mode is therefore 0:
`malloc` returns null on failure and calls no handler.

### The game's operator new and delete

The game supplies its own global `new` and `delete`, each a forwarder to the C runtime:

- `0x00210EC0` is `new`: it presets `r8d = -1` and `edx = 0`, which nothing reads, and jumps to the
  `malloc` stub `0x0085E730`. A `new` expression calls it and tests the result before the constructor
  runs: `0x001D50D0` calls `0x00210EC0(0x10E8)`, stores the result, and calls the constructor `0x001CCB20`
  only when it is not null (`0x001D50FB`). It returns null on failure and throws nothing.
- `0x00210EB0` is `delete(void*)`: a jump to the `free` stub `0x0019C590`.
- `0x00809950` is the sized `delete(void*, size_t)`: a jump to `0x00210EB0`. Scalar deleting
  destructors call it after `test dl, 1` with the object's size in `edx`, for example
  `0x0018D11D` (`mov edx, 8`) and `0x00195551` (`mov edx, 0x98`).
- 48 call sites call the `malloc` stub `0x0085E730` directly after clearing `edx`, the same setup as
  `0x00210EC0` (`0x0017E92C`: `or r8d, -1; xor edx, edx; mov ecx, 0x188`).
- Two more reach `0x0085E730` by tail jump after the same setup: `0x00210EC0` (`0x00210EC6`) and `0x0036D240` (`0x0036D249`,
  after `movsxd rcx, ecx`). `0x0085E690` stores the stub's address, or `rcx` when it is not null, into `0x01F44CE0`
  (`0x0085E693`-`0x0085E6A1`), and the `free` stub `0x0019C590`'s, or `rdx` when it is not null, into `0x01F44CE8`
  (`0x0085E6A8`-`0x0085E6B3`).
- `0x00221770` takes an `int` size, sign-extends it and jumps to `0x00210EC0`.

### Aligned blocks

`_aligned_malloc` is reached only by tail jumps: from `0x0019C580` and from the two EASTL allocate
methods below. `0x0019C580` is `mov edx, edx` (the alignment as a 32-bit value) and the jump.

- `0x0017D260(size, alignment)` presets `r9d = -1` and `r8d = 0` and jumps to `0x0019C580`, so it
  allocates with the caller's alignment.
- `0x00584740(size)` does the same with the alignment materialised as `lea edx, [r9 + 0x11]` from the
  `-1` already in `r9d`, which is 16.
- `0x00584730(p)` frees: `test rcx, rcx` and, when the pointer is not null, a jump to the
  `_aligned_free` stub `0x0019C570`. It is the most called function of this page.

Neither allocate wrapper checks the alignment it passes. Blocks from `0x0017D260`, `0x00584740` and the
EASTL logging allocator go back through `0x00584730`, `0x0019C570` or `0x001EDFE0`; blocks from
`0x00210EC0` go back through `0x00210EB0` or `0x00809950`.

### The standard library's 32-byte rule

The MSVC standard library's allocator reaches `new` and `delete`, not the aligned pair, and aligns
large blocks itself. `0x002099D0(this, count)` allocates `count` 16-byte elements:

1. a count of 0 returns null, and a count above `0x0FFFFFFFFFFFFFFF` calls `_Xbad_alloc`
   (`0x002099EF`), as does a size of 4 KiB or more whose `+0x27` wraps past 64 bits (`0x00209A0C`);
2. below 4 KiB it returns `0x00210EC0(bytes)`;
3. from 4 KiB it allocates `bytes + 0x27` (`0x00209A03`), rounds the result up to 32 bytes
   (`0x00209A27`, `0x00209A2B`) and stores the raw pointer in the qword just below the returned address
   (`0x00209A2F`).

Either path that gets null from `0x00210EC0` calls `_invalid_parameter_noinfo_noreturn`
(`0x00209A20`, `0x00209A45`). Its siblings `0x00209950`, `0x00209A50`, `0x0020D970`, `0x005FEC70`, `0x00783E10`,
`0x007910C0` and `0x00195C70` have the same shape for elements of 4, 24, 12, 8, 32, 8 and 2 bytes.

The matching release `0x001A5A80(this, p, count)` for 8-byte elements repeats the size test: from 4 KiB it
requires `p` to be 32-byte aligned, reads the raw pointer from `p - 8`, requires the difference to
lie between 8 and `0x27`, and frees the raw pointer through `0x00210EB0`; any failed test calls
`_invalid_parameter_noinfo_noreturn`.

### The two EASTL allocator classes

The image carries RTTI for `eastl::allocator` and `eastl::allocator_memory_log`. Both vtables have
six slots:

| Slot | `eastl::allocator` `0x008F6500` | `eastl::allocator_memory_log` `0x00902720` |
|---|---|---|
| 0 | `0x0016D680`, returns `this` | `0x0016D680` |
| 1 | `0x0016D6B0`, `malloc(size)` | `0x001EDF10`, `_aligned_malloc(size, alignment)` |
| 2 | `0x0016D6B0`, the same body | `0x001EDF80`, `_aligned_malloc(size, 16)` |
| 3 | `0x0016D6C0`, `delete(p)` through `0x00210EB0` | `0x001EDFE0`, `_aligned_free(p)` when not null |
| 4 | `0x0016D690`, returns `"EASTL"` (`0x01CDAE78`) | `0x0016D690` |
| 5 | `0x0016D6A0`, `ret 0` | `0x0016D6A0` |

`0x0016D6B0` is `mov rcx, rdx` and a jump to `malloc`: the alignment, offset and flags arguments are
dropped. The containers construct the logging class through `0x001EDF00`, which stores the vtable
`0x00902720` and returns. The plain vtable `0x008F6500` is loaded at five sites, in `0x001A2130`,
`0x001A99B0`, `0x001E1670` and `0x00676BD0` and at `0x006CC33D`.

The site at `0x001A99D5`, in `0x001A9940`, builds a guarded local static at `0x01F81188`: an EASTL tree
whose `0x60`-byte nodes hold two `std::string`s at `+0x20` and `+0x40`, with the plain allocator at
`+0x30`. On first use `0x001A9940` passes it with `/GameData/D3D11/ArtData/shared/phyremaps.txt` to
`0x00677030`, through the jump thunk `0x00677340` (`0x001A998D`). Its `atexit` teardown `0x008A69A0` hands the root to `0x001A49C0`, which walks the nodes,
frees both strings and returns each node through slot 3 of the allocator.

### The memory log that logs nothing

Each of the three memory methods of `allocator_memory_log` begins by testing the pointer
`0x01F82E48`. When it is null, the method takes `malloc(0x20)` and, when that succeeds, writes
`0x2000000` at `+0x00`, `0x200000` at `+0x04`, a zero qword at `+0x10` and a zero dword at `+0x18`
(`0x001EDF3A` to `0x001EDF4F`), then stores the result at `0x01F82E48`, null or not.

The only six instructions that address `0x01F82E48` are these three tests and three stores. No code
reads the record, so the two sizes are never used, the counters never change, and `+0x08`, `+0x0C`
and `+0x1C` keep whatever `malloc` returned. A failed `malloc(0x20)` leaves the pointer null, and the
next call tries again.

### Big blocks at boot

Start-up takes eleven blocks, about 257 MiB, through `0x0036D240`, which sign-extends a 32-bit size
and jumps to the `malloc` stub; nine of them become arenas 2 to 9 and 11. The block table, the slot
counts and the registrar are on the [start-up constants](../Engine-Core/startup-constants.md)
page, and what an arena does with its block is on the
[resource arena page](../Game-Files-And-Data-Tables/resource-arena-and-relocation.md). The boot
routine passes each result to the registrar with no null test.

`0x0036D250` is the matching release: `free` when the pointer is not null. Its one caller, `0x0037B3D0`,
frees arena 11's block and takes a new one of `0x3C0000` or `0x400000` bytes. Arena 7's block is
also used raw: `0x003B0660`, `0x002FC860` and `0x003B2334` pass the block in `0x01FD4A30` itself as the
destination of their resource requests through `0x0032E620`.

The later arenas take their memory from other arenas, not from the heap:

- `0x0025A990` selects arena 5, takes `0x100000` bytes top-down with `0x0036A190`, labels the block
  `EVTMEM` and registers it as arena 13; `0x0025AA30` does the same with `0x19000` bytes labelled
  `SMNMEM` for arena 14. Each first releases the block it built before, and skips the registration
  when the allocation returns null.
- `0x003E9AA0(arena, size)` takes arena 12's block top-down from the arena it is given, or from arena 6
  when the argument is negative. A null result spins forever at `0x003E9AE0`.

### The machine's memory: the file-cache budget and the working set

`0x001D6BE0`, called once from `0x0017D6B0`, runs `0x0020C610` and then `0x0020C6B0`. `0x0020C610` reads
`GlobalMemoryStatusEx` and sets the budget `0x01F83448` to a third of the physical memory, at least
`0x2000000` (32 MiB) and capped at `0x100000000` (4 GiB) when the third exceeds `0xFFFFFFFF`. It sets
`0x01F83441` to 1 when the physical memory is below 1 GiB and to 0 otherwise, and sets `0x01F83440` to 1.

`0x0020C6B0` creates the RAM file cache manager once: `0x00210EC0(0x158)`, constructed by
`0x0020B2E0(manager, budget)` and kept at `0x01F83438`. The constructor stores the budget as the
manager's limit `+0x00` and builds its pool of `0x18`-byte cache entries at `+0x98` with
`(budget >> 31) × 10,000` entries, at least 10,000 and at most 1,000,000; with a budget of at most
4 GiB that is 10,000, or 20,000 when the budget is 4 GiB.

The cache's own allocator sits on `malloc`: `0x0020B130(manager, size)` returns null when the usage
`+0x10` is above the limit, and otherwise adds the size to the usage with `lock xadd` and jumps to
`malloc`; `0x0020B0F0(manager, p)` subtracts `_msize(p)` (the only `_msize` call in the image,
`0x0020B103`) and jumps to `free`. How the cache evicts when this allocator refuses, and how the two
flags steer file reads, is on the
[file path resolution](../Game-Files-And-Data-Tables/file-path-resolution.md) page.

The second reader of `GlobalMemoryStatusEx` is `0x00792F10`, the constructor of
`Phyre::PFramework::PWindowWin32Base`. It sets the process priority class to
`ABOVE_NORMAL_PRIORITY_CLASS` (`0x8000`, `0x00792F80`), reads the page size and the physical memory,
and calls `SetProcessWorkingSetSize` with the current minimum (50 pages when
`GetProcessWorkingSetSize` fails) and a maximum of the physical memory less 512 pages, less 1
(`0x00792FD9` to `0x00792FE8`).

### The actor record pool

An actor manager carves all its records out of one block. `0x002679F0(manager)`, called once from
`0x0026CE60`, reads the definition data `L` at manager `+0x00`: a row count (u16 at
`L + [L + 0x14]`) followed by one u16 record count per row. Each row's record size comes from the
eight-row table at `0x01E0C328`. The block size is

```python
header = (n * 8 + 0x17) & ~0xF            ; n = manager +0x20, the total record count
total = 2 * header + sum over rows of round16(size[row]) * count[row]
```

It takes the block through the function pointer at manager `+0x88` (`0x00267A79`), clears it with
`memset` (`0x00267A8B`) without a null test, writes `n` at `+0x00` and points manager `+0x1F0` at
`block + header`. The records follow from `block + 2 * header`, each rounded up to 16 bytes, and
the record pointers fill `block + 0x08` onward.

Every record's byte `+3` is set to `(row & 0x1F) | (class << 5)`, the class being the table's byte
`+0`; an earlier write of the same byte in the loop is overwritten at once. The record counts per
class are added to the four words at manager `+0x1D0`, and `+0x1D8` receives their running starts.
`0x00266530` then initialises each record. A record is an interior pointer: only the block itself can
be freed.

The block function is installed by `0x0026C8C0`, which stores `0x00267930` or its third argument at
manager `+0x88` (`0x0026CAE6`). Its one caller, `0x0032F850`, passes one of three hooks. Each selects an
arena, allocates with `0x0036A100`, labels the block with `0x0036C660` and the source file name
`ateldecode.c`, and pops the selection:

- `0x00267930` uses arena 5 and the label tag `0x1676`;
- `0x00267BB0` uses arena 13 when it is enabled (`0x0036B200(13)` tests its bit in `0x022D89B8`), else
  arena 5, with tag `0x16C1`;
- `0x00267C20` uses arena 14 when enabled, else arena 5, with tag `0x16E6`.

`0x0032F850` picks the hook from the low four bits of its argument: 1 and 2 give `0x00267BB0` and 3
gives `0x00267C20` when arena 13 or 14 is enabled; every other case gives `0x00267930`.

### The movie player's ring buffers

`0x006CC5A0(ring, size, extra, alloc, free)` builds a ring buffer that takes its allocator as
arguments. It stores `size + 0x20` at `+0x4C` and the release function at `+0x58` (`0x00584730` when
none is given), allocates `size + 0x20 + extra + 0xF` bytes with `alloc` (`0x00584740` when none is
given) into `+0x08`, sets `+0x10` to `size + 0x10` and zeroes the dword there, and returns whether
the block is non-null.

Its three calls pass the pair held in the static cells `0x01F2EAA8` (`0x00584740`) and `0x01F2EAB0`
(`0x00584730`), so the rings come from the 16-byte aligned heap. The
[movie player](../Third-Party-Libraries/media-decoder-libraries.md) makes them:

- `0x00679A50`, the Vorbis start, builds an `0x800000`-byte ring at `+0x150` with `extra` =
  `[+0x324] << 13` (`0x00679B93`), then takes `[+0x324] × 48,000 × 4` bytes directly from `0x00584740`
  for its output buffer at `+0x4E8` and clears it (`0x00679BA5`).
- The movie open `0x0067A480` builds a `0x2000000`-byte ring at `+0x00` (`0x0067A826`) and a second one
  at `+0xA8` (`0x0067A857`), both with `extra` = `[+0x524] + [+0x524] / 2`; the second ring's size is
  `(extra + 0x10) × [+0x2F0]`.

The cells are initialised data in the image; no instruction writes them.

### The asset-name registry beside the hook pair

The six qwords at `0x01F2EA70`, just before the pair, are the head of an ordered tree of named Phyre
`PAssetReference` objects; its accesses are listed in
[`memory-and-allocation-p-asset-reference-registry-01f2ea70-accesses.tsv`](memory-and-allocation-p-asset-reference-registry-01f2ea70-accesses.tsv).
The head is six qwords that point at `0x01F2EA70` when the tree is empty, with the root at `+0x18`.
It is built on first use, under the lock `0x02D3E880`, by a guarded one-time initialiser
(`0x02D3EC9C`) that also registers `0x008B1C00` with `atexit`; that destructor clears the tree through
`0x0067F580`.

- `0x00677BA0(object)` registers one object. A null name at `+0x30` (bit 0 masked off) returns `0x15`.
  Otherwise it resets the node at `+0x08`, stores the name's hash (`0x00677350`, seed `0x7B5`) at
  `+0x20` and the name at `+0x28`, looks the object up with `0x006750C0`, and inserts it with
  `0x0067F700`; an object whose name is already present returns `0x12`.
- `0x00675460(object)` removes one: when the object is linked it erases the node under the same lock
  (`0x0067FE20`), then frees an owned name at `+0x30` (bit 0 clear) with `0x00584730`. It is reached
  through `0x00674A30`, slot 11 of the three `PAssetReference` class-descriptor vtables `0x00D6BA78`,
  `0x00D6BB00` and `0x00D6BB88`.

The qword `0x01F2EAA0` between the head and the pair holds 2. Its one reader, `0x00677030`, reads a text
file into a block two bytes longer than the file, zeroes the two extra bytes, and uses the same
value as the length of its `"\r\n"` comparison when it splits the text into lines.

### When an allocation fails

- `malloc`, `calloc` and `realloc` return null; the new mode is 0, so no handler runs.
- `new` (`0x00210EC0`) returns null and constructs nothing; `new` expressions test before the
  constructor.
- The standard library allocator calls `_invalid_parameter_noinfo_noreturn` on a null and
  `_Xbad_alloc` on an oversized count; `_Xbad_alloc` is called at 23 sites in 14 functions in all.
- `realloc`'s five call sites, in `0x00203490`, `0x00204DA0`, `0x00204E50` and `0x00205384`, grow the
  standard library's regular-expression character buffer by 16 bytes and call `_Xbad_alloc` on a
  null.
- The boot blocks and the actor pool use the result without a test.
- Arena 12's setup spins forever; arenas 13 and 14 stay unregistered.
- The file cache refuses over its budget, evicts and retries; the arena allocator's own retry is on
  the [resource arena page](../Game-Files-And-Data-Tables/resource-arena-and-relocation.md).

## Layouts

Memory log record   `0x01F82E48` -> malloc(`0x20`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | budget | `0x2000000`, never read |
| `+0x04` | `u32` | block | `0x200000`, never read |
| `+0x08` | `u32` | (none) | never written |
| `+0x0C` | `u32` | (none) | never written |
| `+0x10` | `u64` | total | 0, never read |
| `+0x18` | `u32` | count | 0, never read |
| `+0x1C` | `u32` | (none) | never written |

Actor record size table   `0x01E0C328`, 8 rows of 4 bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | class | 0 to 3; indexes the manager's words `+0x1D0` and the record's byte +3 |
| `+0x01` | `u8` | (none) | 0 or 1; read by nothing |
| `+0x02` | `u16` | size | record bytes before rounding to 16 rows   0: class 0 `0x328`   1: class 1 `0x3A8`   2: class 1 `0x330`   3: class 2 `0x348` 4: class 2 `0x2D0`   5: class 3 `0x6E0`   6: class 3 `0x6E0`   7: class 3 `0x668` |

Actor pool block:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | n, the record count |  |
| `+0x08` | `void*` | record pointers, n entries | +header           -    manager `+0x1F0` points here +2*header         -    records, each round16(size) bytes, in row order |

Ring buffer (`0x006CC5A0`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x08` | `void*` | block | from the alloc argument |
| `+0x10` | `u32` | size + 0x10 | the dword at block + this value is zeroed |
| `+0x14` | `u32` | 0 | `+0x28`, `+0x38`               two objects set up by `0x005CD0E0`(p, 1) |
| `+0x4C` | `u32` | size + 0x20 |  |
| `+0x58` | `void*` | release function |  |

Static block `0x01F2EA70`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*[6]` | registry tree head, self-pointing when empty; root at +0x18 |  |
| `+0x30` | `u64` | 2, the line-terminator length read by 0x00677030 |  |
| `+0x38` | `void*` | 0x00584740, allocate 16-byte aligned |  |
| `+0x40` | `void*` | 0x00584730, aligned free |  |

The file cache manager's other fields are on the
[file path resolution](../Game-Files-And-Data-Tables/file-path-resolution.md) page.

## Shipped data

Imports, call sites of the allocation routines, and the boot blocks, in the executable.

| Fact | Value |
|---|---|
| Import symbols | 538, from 30 DLLs |
| Heap imports | 8, slots `0x008C2B40` to `0x008C2B78` |
| Direct `call [malloc]` / `call [free]` | 30 / 37 |
| `0x00584730` aligned free | 2,596 calls and 1 jump, in 2,308 functions |
| `0x0017D260` aligned allocate | 281 calls and 2 jumps, in 226 functions |
| `0x00584740` 16-byte allocate | 45 calls, in 29 functions, and the cell `0x01F2EAA8` |
| `0x00210EC0` new | 257 calls and 1 jump, in 180 functions |
| `0x00210EB0` delete | 316 calls and 25 jumps, in 239 functions |
| `0x00809950` sized delete | 502 calls and 6 jumps, in 473 functions |
| `0x0085E730` `malloc` stub | 48 calls and 2 jumps |
| `0x0019C570` `_aligned_free` stub | 17 calls and 1 jump, in 4 functions |
| `0x001EDF00` EASTL allocator constructor | 583 calls, in 230 functions |
| `calloc` stub `0x00861FBC` | 30 calls, in 16 functions from `0x00880230` to `0x00893E80` |
| `realloc` / `_msize` | 5 / 1 direct calls |
| `_Xbad_alloc` | 23 calls, in 14 functions |
| Boot blocks | 11, `0x10120930` bytes (257.1 MiB) |
| Actor record size rows | 8 |

## State

The heap state lives in the C runtime. The game keeps the boot block pointers (`0x01FD49F0` to
`0x01FD4A40`, `0x01FD4A18`, `0x01FD4A20`, `0x01FD4A90`), the memory-log pointer `0x01F82E48`, the file-cache
budget `0x01F83448`, its flags `0x01F83440` and `0x01F83441` and manager `0x01F83438`, the registry head
`0x01F2EA70`, and each actor manager's block pointer, class counts and hook.

## Modding notes

- Hooking the import slots `0x008C2B40`, `0x008C2B48`, `0x008C2B60` and `0x008C2B70` catches every route on
  this page at once, including the arenas' boot blocks.
- To redirect only the game's own wrappers, patch `0x00210EC0`, `0x00210EB0`, `0x0017D260`, `0x00584740`
  and `0x00584730` together; the two EASTL vtables live in read-only data and the forwarder chains
  (`0x00809950` to `0x00210EB0` to `0x0019C590`) must be followed or hooked at their end.
- Release a block with the family that allocated it: aligned blocks through `0x00584730`, `new`
  blocks through `0x00210EB0`, standard-library blocks of 4 KiB or more only through `0x001A5A80` or its
  siblings, which recover the raw pointer.
- Never free an actor record; only the pool block is a block.
- A record kind larger than its row in `0x01E0C328` overruns the next record; the table has exactly
  eight rows, and a definition with more rows reads past it.
- The memory-log record is not a budget: writing to it changes nothing.
- The file cache's limit comes from physical memory at start-up; changing `0x01F83448` afterwards
  does not resize the entry table.

## Related

- [Resource arenas and relocation](../Game-Files-And-Data-Tables/resource-arena-and-relocation.md): the fifteen arenas built on the boot blocks.
- [Start-up constants](../Engine-Core/startup-constants.md): the boot block table and the arena registrar.
- [File path resolution](../Game-Files-And-Data-Tables/file-path-resolution.md): the RAM file cache this page sizes.
- [Media decoder libraries](../Third-Party-Libraries/media-decoder-libraries.md): the movie player that owns the ring buffers.
- [Jump thunks](../Engine-Core/jump-thunks.md): the forwarders, including the `free` chain.
- [Game application](../Engine-Core/game-application.md): the init job that runs the boot routines.
