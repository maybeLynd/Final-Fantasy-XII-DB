---
title: "Bigfile archive: the VBF container, how its index loads and is checked, and how a read reaches the file"
kind: "system"
category: "Game files and data tables"
addresses: "0x0017CEB0, 0x0019B070, 0x001F4340, 0x001F4120, 0x001F4720, 0x001F3FD0, 0x0019AEE0, 0x001F47D0, 0x001F4250, 0x00214FC0, 0x00215290, 0x00215110, 0x0019AFE0, 0x0019A770, 0x0019A860, 0x0019AA20, 0x0080C5A0, 0x01F81110, 0x009038C8, 0x008C2140, 0x008C2EF0, 0x0017D280, 0x008098D4, 0x007A0A80, 0x001F4060, 0x002150B0, 0x001F4840, 0x00215220, 0x0019B200, 0x0019A660, 0x0019A6E0, 0x0019A9B0"
---

## What the player sees

The game's data lives in one 31 GB file, `FFXII_TZA.vbf`, in the game folder beside the `x64` folder that
holds the program. It opens at once
at start-up, because only its index is read and checked; the data itself is read a piece at a time
as the game needs it. An edited index the game does not accept leaves the archive unmounted, and every
file the game then asks for fails to open. A compressed block that fails to inflate shows a Windows
error box, "Broken game data, please repair or restore the data."

## How it works

### Mounting

`0x0017CEB0` sets the base path (`0x0059A770("../../..")`), calls `0x0019B190`, and mounts
`"../FFXII_TZA.vbf"` into the archive manager from `0x0019B1F0` with `0x0019B070`; it never tests the
result. `0x0019B070(manager, path)` puts a new `0xB0`-byte archive object in the first empty one of the
manager's five slots `+0x20..+0x40` and opens it with `0x001F4340`; when the open fails it destroys and
frees the object (`0x001F4120`) and clears the slot. With all five slots full it returns false without
opening anything. `0x0017CEB0` is the only caller of `0x0019B070`, so the shipped game fills slot 0 only.

`0x0019B070` allocates the object with `0x00210EC0` (`0x0019B0B4`) and returns the opener's result; when that
allocation returns null, the slot stays 0 and it returns false without opening anything (`0x0019B0D0`,
`0x0019B0DD`). After a failed open it frees the `0xB0` bytes with `0x00809950` (`0x0019B10A`) and clears the slot
(`0x0019B10F`). With all five slots full it returns false from `0x0019B0AD`. Its one call is at `0x0017CEF6`.

`0x001F4060` constructs the object: an empty key tree whose
nodes come from a `PMapPair` allocator (`0x0067FFB0`, `0x30`-byte nodes), null tables and handles, and the
critical section `+0x80`. The nulls are the index `+0x00` (`0x001F407D`), the block-size table `+0x68`, the
`+0x70` array, the path `+0x78` and the handles `+0xA8` (`0x001F40C2`-`0x001F40CE`); the block count `+0x60` is
left unwritten. It returns the object (`0x001F40E2`).

`0x001F4120` destroys it: it deletes the critical section `+0x80` (`0x001F413B`), and `0x001F41A0` frees the path
`+0x78`, the index `+0x00` and the `+0x70` array, each only when set, and zeroes it; then it destroys each of
the handles at `+0xA8` (`0x00215040`: window freed, file closed), frees their array and zeroes `+0xA8`. It then
erases the tree's nodes one by one (`0x0067FE20`, `0x001F4161`), frees the node pool's blocks (`0x006803D0`,
`0x00680030`) and calls `0x0067F580` on the tree twice (`0x001F4180`, `0x001F4189`).

### Loading and checking the index

`0x001F4340(archive, path)` copies the path into a 260-byte buffer (`+0x78`) and opens it with CRT
`fopen(path, "rb")`; a null path or a failed `fopen` returns false. It reads the magic and refuses
anything but `0x4B595253` (`'SRYK'`): it logs `"BigFile head wrong!\n"` (`0x009038C8`) through `0x0017D280`
and returns false without closing the file. It reads `indexSize` (the second dword), seeks 16 bytes
before the end and reads the stored digest there, then reads the first `indexSize` bytes of the file
in one `fread` into `+0x00` and closes the file.

It hashes that buffer with MD5 (`CryptCreateHash`, `0x8003`) and compares the two 64-bit halves with
the stored digest; on a mismatch it returns false with no message. None of the six CryptoAPI results
is tested; only the digest buffer is compared. The digest covers the header, keys, records, names and
block-size table, and nothing after `indexSize`: the payload lies outside the check.

### Parsing the index

After the check the opener:

1. Finds the record array after the keys, the name table after the records, and the block-size
   table after the names (`+0x68`).
2. Computes the block count `+0x60` from the last record: its first block plus `size >> 16`, plus one
   when `size & 0xFFFF` is non-zero.
3. Builds a one-byte-per-block array at `+0x70`: 0 where the block-size entry is 0, otherwise 1; then,
   for each entry, its last block is set to 0 when the entry's block-size value equals
   `size & 0xFFFF`.
4. Rebases each record's `nameOffset` to a pointer (adding the name table's start) and inserts the
   record under its key into a red-black tree at `+0x08` (`0x001F4720` → `0x001F3FD0`); nodes hold the key
   at `+0x18` and the record pointer at `+0x28`, ordered by the halves as signed 64-bit values, `+0x18`
   first and `+0x20` on a tie (`0x001F4008`-`0x001F4028`).
5. `0x001F4720` takes a node from the pool's free list (refilled by `0x00680150` when empty, `0x001F4755`), copies
   the key and the record pointer in, has `0x001F3FD0` link it as a leaf under the last node of the walk
   (`0x001F4055`), rebalances (`0x0067F700`) and returns 0.
6. A key already in the tree is not inserted again: `0x001F3FD0` returns the node that holds it (`0x001F4028`,
   `0x001F405C`), `0x001F4720` puts the new node back on the free list (`0x00680200`) and returns `0x12`, and the
   opener ignores the result (`0x001F4677`), so the first record with that key is the one a lookup finds. A
   free list still empty after the refill returns `0xE` with nothing inserted (`0x001F47B8`).
7. Allocates fifteen `0x30`-byte reader handles (`0x2D8` bytes, a count of 15 first) at `+0xA8`, and
   opens the archive in each one (`0x00215290`).

### Finding a file

`0x0019AEE0(manager, name)` returns 0 when the manager pointer `0x01F81110` is null. Otherwise it
MD5-hashes the name from offset `[manager + 0x70]` and asks each filled slot in order 0 to 4 through
`0x001F47D0(archive, digest)`; the first hit wins. The hash comes from the CryptoAPI provider at
`[manager + 0x00]` (`0x0019AF38`-`0x0019AF79`), with no result tested. A slot whose call returns 0 passes the
search to the next one; with no slot left it returns 0 (`0x0019AF6B`, `0x0019AFB5`), and it destroys the hash
before returning (`0x0019AFAF`).

`0x001F47D0` walks the tree with the same signed order
and hands the record to `0x001F4250` (a tail jump, `0x001F4834`); a miss returns 0 (`0x001F4839`). `0x001F4250`
takes the first free handle of the fifteen under the archive's lock (`+0x80`) and binds it there
(`0x002150B0`, `0x001F42B7`). When all fifteen are busy it builds a fresh handle for that open
(`0x008098D4(0x30)`, `0x00214FC0`, `0x00215290`), which never joins the pool. The lookup never compares
names. When that allocation returns null, `0x001F4250` returns 0 (`0x001F42F9`, `0x001F4318`), and `0x0019AEE0`
goes on to the next slot as after a miss.

`0x00214FC0` clears the in-use byte, the archive, the record and the position, leaves the file `+0x08` for
`0x00215290`, and gives the handle a `0x18`-byte window holding a 64 KiB buffer and both bounds 0
(`0x00214FF0`-`0x00215013`). When the window's allocation returns null the window pointer `+0x28` is 0
(`0x00215019`), and the bind's write to the window's bounds (`0x002150BE`) faults at address `0x10`.

`0x00215290(handle, path, archive)` opens the archive's path `+0x78` with `fopen(path, "rb")`, stores the
result at `+0x08` without testing it (`0x002152B3`), and stores the archive at `+0x10` when it is not null
(`0x002152B7`).

`0x002150B0(handle, record)` binds a handle: it stores the record at `+0x18`, sets the position `+0x20`
and the window's bounds to 0 and the in-use byte `+0x00` to 1. The resolver takes the file's size from
the record through `0x00215280`.

Closing a stream releases its handle through `0x002150D0` →
`0x001F4840(archive, handle)`: a handle of the fifteen is cleared (`0x002152D0`: record, position and
in-use byte), and any other is destroyed (`0x00215040`: frees its 64 KiB window and closes its file) and
freed (`0x00809950`, `0x30` bytes, `0x001F488F`). A null handle returns at once (`0x001F4843`), and the release
does not enter the lock `+0x80`.

### Reading bytes

A handle read `0x00215110(handle, buffer, n)` takes n as 32 bits, clamps it to `size − position` when the
read would pass the entry's size (returning 0 when nothing is left), serves what it can from the handle's
64 KiB window, and passes the rest to the archive reader `0x0019AFE0`.

The clamp is a 32-bit difference, `n = (uint32)size - (uint32)position` when `position + n > size`
(`0x00215143`, `0x00215149`-`0x0021514C`): with the position past the size, `position > size`, the difference wraps,
and unless it is 0 the read goes on with that length.

The window `+0x28` holds the entry's bytes from the position at its `+0x10` up to the one at its `+0x08`,
in the buffer at its `+0x00`. A request inside it is copied with `memcpy` (`0x00215182`) and returns n
without calling `0x0019AFE0`. One that starts inside it and runs past its end copies the window's part first
(`0x002151A5`); one that starts before it and ends inside it copies its last bytes from the window
(`0x002151D3`).

The rest of the request, or all of any other one, is read through
`0x0019AFE0(0x0019B1F0(), buffer, count, handle, position, handle +0x10)` (`0x002151F9`), and the result is that
return plus the bytes copied (`0x002151FE`). The read stores nothing in the handle: its caller `0x002150E0`
adds a non-zero result to the position `+0x20` (`0x002150F4`).

A handle seek `0x00215220(handle, offset, origin)` sets the position to the offset (origin 0), adds
the offset (1) or sets it to the size minus the offset (2), and returns the new position, or
`FFFFFFFF` for another origin. It tests only the offset argument: a negative offset or one above the
size returns `FFFFFFFF` after the position has changed, and origin 1 can move the position past the
size. The offset is a signed 32-bit value (`0x00215220`), another origin leaves the position unchanged
(`0x00215235`), and the position comes back as its low 32 bits (`0x0021526A`).

`0x0019A770(manager, buffer, n, handle, position, archive)` plans a read: starting at the record's
`firstBlock` and its archive `offset` (`0x0019A7AB`, `0x0019A7AE`), it skips
whole 64 KiB blocks by adding each skipped block's stored size (a block-size value of 0 counts as
`0x10000`). It skips `position >> 16` of them (`0x0019A7C2`) and takes a read record from `0x0019A6E0` with
the start `position & 0xFFFF`, block `0x10000` and n (`0x0019A805`).

The planner stores in the record the block reached `+0x04`, the archive offset `+0x48`, the skipped bytes
`+0x50`, n `+0x58`, the buffer `+0x28`, the handle's window `+0x20`, the entry `+0x60`, the archive `+0x68`
and the handle's file `+0x70` (`0x0019A817`-`0x0019A848`), and returns the record.

`0x0019A860` seeks there (`_fseeki64`) and reads the stored blocks with CRT `fread`. It sets the state
`+0x88` to 1 (`0x0019A887`), seeks the file `+0x70` to `+0x48` from the start (`0x0019A8A2`), and from block
`+0x04` on reads each block with one `fread` of its stored size (0 read as `0x10000`):

- the head block into the head part's buffer, when the head is used (`0x0019A8D1`);
- when the middle is used, every full middle block but the last into the buffer `+0x28`, one block ahead
  of its place: middle block k at the head's length plus `0x10000` × (k + 1) (`0x0019A91E`); the last one
  into the middle part's buffer (`0x0019A951`);
- the tail block into the tail part's buffer, when the tail is used (`0x0019A982`).

It tests no result and sets the state to 2 (`0x0019A98D`).
`0x0019AA20` turns each block into 64 KiB (or the tail's length): a block whose `+0x70` byte is 0 is
copied as stored, any other is inflated with zlib 1.2.11's `uncompress` (`0x0080C5A0`).

`0x0019AA20` ORs every `uncompress` result. When any is non-zero, or the bytes produced do not total the
request `+0x58` (`0x0019ADD1`-`0x0019ADDA`), it loads string-table text `0x7834` (`0x0019A510`,
[Steam integration](../Steam-And-Achievements/steam-integration.md)) into a `SysAllocStringLen`
copy (`0x0019AE06`), calls `0x007A0A80(1)` (`0x0019AE1D`), shows the copy with `MessageBoxW` and the icon flag
`0x10` under the caption "error" (`0x008F3DC0`, `0x0019AE34`), sets the read's state `+0x88` to 6
(`0x0019AE3A`) and frees the copy (`0x0019AE47`); otherwise the state becomes 5 (`0x0019ADDC`).

`0x007A0A80(1)` frees the cursor clip (`0x0079ED60(1)`, `0x007A0A89`), reads the cursor state with
`GetCursorInfo` (`0x007A0A9F`) and, when its flags are 0, shows the cursor with `ShowCursor(1)` and sets
`0x01F3DA06` to 1 (`0x007A0AB7`, `0x007A0ABD`). Given 0, it hides a cursor whose flags have bit `0x1` with
`ShowCursor(0)` and sets the byte to 0 (`0x007A0ACA`-`0x007A0ADB`).

### Read records

The manager `0x01F81110` (`0x80` bytes, `0x0019B190` → `0x0019AE70`) holds thirty read records of `0x98`
bytes built by `0x0019B200(manager + 8, 30)`, which constructs each with `0x0019A3B0` (`0x0019A2A0`: three
part descriptors, each with its own 64 KiB buffer) and creates a semaphore with thirty counts.

`0x0019B200(bank, count)` stores the count at `bank + 0x08` (`0x0019B219`). It first destroys and frees a
record array already at `bank + 0x10` (`0x00809054` with `0x0019A500`, `0x00809950`) and closes a semaphore
already at `bank + 0x00` (`CloseHandle`, `0x0019B2BC`). The new array is `count × 0x98` bytes after an 8-byte
count (`0x00210EC0`, `0x0019B27A`); when that allocation returns null the array pointer is 0 (`0x0019B2AE`). The
semaphore, `CreateSemaphoreW(NULL, count, count, NULL)`, goes to `bank + 0x00` untested (`0x0019B2DA`).

- `0x0019A660` waits on the semaphore, then claims the first record whose busy word `+0x90` it can
  change from 0 to 1 atomically, and raises its use count `+0x40`. The semaphore, the record count and
  the array are the manager's `+0x08`, `+0x10` and `+0x18` (`0x0019A66C`, `0x0019A680`, `0x0019A690`).
- When the wait does not return 0 (`0x0019A67B`), when the count is 0, or when no busy word changes,
  `0x0019A660` raises the use count through a null record: the write to address `0x40` faults (`0x0019A6C6`,
  `0x0019A6B2`). With a null array the exchange at `0x0019A69F` faults at address `0x90`.
- `0x0019A6E0(manager, start, block, n)`, `block` = `0x10000`, takes a record that way and sets its state
  `+0x88` to 0 (`0x0019A700`). With `start`
  not 0 it marks the head used with offset `start` and length `head = min(block - start, n)`, an unsigned
  64-bit min (`0x0019A713`-`0x0019A71F`), then `n -= head` in 32 bits (`0x0019A736`).
- `0x0019A6E0` marks the middle used when `n >= block`
  (`0x0019A739`-`0x0019A741`) and the tail used with length `n % block` when that is above 0
  (`0x0019A744`-`0x0019A759`), and returns the record.
- After the read, `0x0019A9B0` lowers the use count under the manager's critical section `+0x48`; at 0
  it resets the record (`0x0019B130`), clears the busy word and releases one semaphore count (the manager's
  `+0x08`, `0x0019A9F7`). A null record returns at once (`0x0019A9B3`).

`0x0019AFE0(manager, buffer, n, handle, position, archive)` plans the read (`0x0019A770`), fills it
(`0x0019A860`), finishes it (`0x0019AA20`) and releases the record (`0x0019A9B0`) whatever the state.
`0x0019AFE0` returns the byte count it was asked for when the read's state is 5 and 0 otherwise
(`0x0019B033`). Its null test of the planner's record (`0x0019B011`) never branches: `0x0019A660` writes
through the record before returning it (`0x0019A6B2`, `0x0019A6C6`).

The import table has no `CreateFileMapping` or `MapViewOfFile`. `ReadFile` (`0x008C2140`) has three
call sites (`0x0059A9B0`, `0x0059D4B0`, `0x0059F4A0`), `SetFilePointer` two and `CreateFileA` two (the
minidump writers `0x005CCAB0` and `0x0079B1E0`); CRT `fread` (`0x008C2EF0`) has 17, including
`0x001F4340` and `0x0019A860`.

## Layouts

### Index

The file starts with the index; `indexSize` bytes of it are covered by the digest.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | magic | `'SRYK'` |
| `+0x04` | `u32` | indexSize | |
| `+0x08` | `u32` | count | entries |
| `+0x0C` | `u8[4]` | zero | copied whole with the index by the opener `0x001F4340` (`fread`); no instruction of the opener, the tree functions `0x001F4720`, `0x001F3FD0` and `0x001F47D0`, the handle taker `0x001F4250` or the planner `0x0019A770` reads or writes it; nothing fixes its width |
| `+0x10` | `u8[16]` | keys | one per entry: the MD5 of its name |

After the keys come `count` entry records, then the names (a `u32` length that counts itself, then
NUL-terminated lower-case names), then one `u16` block size per 64 KiB block up to `indexSize`: 0 for a full
raw block, `size & 0xFFFF` in an entry's last block for a raw tail, otherwise the length of a zlib stream.
The last 16 bytes of the file are the MD5 of `[0, indexSize)`.

### Entry record

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | firstBlock | |
| `+0x04` | `u8[4]` | firstBlock copy | copied whole with the index by `0x001F4340`; no instruction of the opener, the tree functions `0x001F4720`, `0x001F3FD0` and `0x001F47D0`, the handle taker `0x001F4250`, the planner `0x0019A770` (which reads only `firstBlock` and `offset`, at `0x0019A7AB` and `0x0019A7AE`) or the handle readers `0x0019A660`, `0x0019A6E0`, `0x0019A860`, `0x0019A9B0` and `0x0019AFE0` reads or writes it; nothing fixes its width |
| `+0x08` | `u64` | size | uncompressed |
| `+0x10` | `u64` | offset | archive offset of the first stored block |
| `+0x18` | `u64` | nameOffset | from the first name |

### Archive object

`0xB0` bytes.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | index | |
| `+0x08` | `KeyTree` | keys | |
| `+0x60` | `u32` | block count | |
| `+0x68` | `u16*` | block sizes | |
| `+0x70` | `u8*` | compressed | one byte per block: 0 raw, 1 zlib |
| `+0x78` | `char*` | path | a 260-byte copy |
| `+0x80` | `CRITICAL_SECTION` | lock | |
| `+0xA8` | `ReaderHandle*` | handles | the fifteen reader handles |

### Reader handle

`0x30` bytes.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | in use | |
| `+0x08` | `FILE*` | file | |
| `+0x10` | `void*` | archive | |
| `+0x18` | `void*` | record | the entry record |
| `+0x20` | `u64` | position | |
| `+0x28` | `Window*` | window | a 64 KiB buffer, its end at `8` and its start at `10` |

### Read record

`0x98` bytes, thirty of them.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x04` | `u32` | block | the first block read |
| `+0x08` | `Part*` | head | |
| `+0x10` | `Part*` | middle | |
| `+0x18` | `Part*` | tail | |
| `+0x20` | `Window*` | window | the handle's window (handle `+0x28`), stored by the planner `0x0019A770` (`0x0019A830`) |
| `+0x28` | `u8*` | buffer | the caller's buffer, stored by the planner (`0x0019A817`); `0x0019A860` reads every middle block but the last into it (`0x0019A91A`) |
| `+0x30` | `u32` | owned | non-zero: the reset frees the buffer at `38`; zeroed by `0x0019A2A0` and the reset `0x0019B130` |
| `+0x38` | `void*` | buffer | freed with `free` while `30` is non-zero |
| `+0x40` | `u32` | use count | |
| `+0x48` | `u64` | archive offset | |
| `+0x50` | `u64` | skipped | bytes in whole blocks skipped |
| `+0x58` | `u32` | length | the request |
| `+0x60` | `void*` | entry | the entry record the request reads from (the handle's `18`), stored by the planner `0x0019A770` |
| `+0x68` | `void*` | archive | stored by the planner (`0x0019A838`); `0x0019A860` takes the block-size table `+0x68` from it (`0x0019A873`, `0x0019A891`) |
| `+0x70` | `FILE*` | file | the handle's file (handle `+0x08`), stored by the planner (`0x0019A848`); `0x0019A860` seeks and reads it (`0x0019A87A`) |
| `+0x88` | `u32` | state | `0` taken (`0x0019A700`), `1` while `0x0019A860` reads (`0x0019A887`), `2` read (`0x0019A98D`), `3` set by `0x0019AA20` on entry (`0x0019AA47`), `5` done, `6` failed |
| `+0x90` | `u32` | busy | |

### Part

`0x18` bytes.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | used | |
| `+0x08` | `u8*` | buffer | 64 KiB |
| `+0x10` | `u32` | length | |
| `+0x14` | `u32` | offset | within the block |

The reader's own records and banks are listed field by field in
[`bigfile-archive-slow-reader-manager-accesses.tsv`](bigfile-archive-slow-reader-manager-accesses.tsv),
[`bigfile-archive-slow-reader-record-bank-accesses.tsv`](bigfile-archive-slow-reader-record-bank-accesses.tsv),
[`bigfile-archive-slow-reader-record-accesses.tsv`](bigfile-archive-slow-reader-record-accesses.tsv) and
[`bigfile-archive-slow-reader-block-descriptor-accesses.tsv`](bigfile-archive-slow-reader-block-descriptor-accesses.tsv).

## Shipped data

| Fact | Value |
|---|---|
| file size | 31,196,932,183 bytes |
| error text | string `0x7834` in nine languages; English "Broken game data, please repair or restore the data." |
| `indexSize` | 11,995,716 bytes; MD5 matches the last 16 bytes |
| entries | 89,414; 89,388 with bytes and 26 of size 0 (`jsondata/cutscenes/*.json`) |
| keys | all 89,414 equal the MD5 of their entry's name; every name is lower case |
| `+0x04` | equals `+0x00` in all 89,388 entries with bytes |
| offsets | each entry starts where the one before it ends, from `indexSize` to 16 bytes before the end |
| blocks | 957,553 (the last entry's first block plus its block count); 189,861 full raw blocks; 1,697 entries end in a raw tail |
| top folders | `gamedata` 39,653, `ps2data` 39,578, `prefetchdata` 9,351, `jsondata` 832 |
| extensions | `.phyre` 35,984, `.txt` 10,253, `.ebp` 10,045, `.sab` 4,609, `.mot` 4,392, `.efx` 3,288, `.ca` 3,164, `.dat` 2,948, `.ah` 2,564, `.snd` 2,304 |

## Operations

At start-up: one 12 MB read, one MD5 over it and one tree insert per entry. Per file open: one MD5 of
the path, one tree walk per mounted archive and one handle. Per read: one seek and one `fread` per
stored block, and one inflate per compressed block.

## State

The archive manager at `0x01F81110` with its five slots; each archive's index buffer, key tree, block
tables and reader handles.

## Modding notes

To repack `FFXII_TZA.vbf` so that the game accepts it:

- Give every entry a key equal to the MD5 of its lower-case name with forward slashes.
- Keep an entry's blocks consecutive from `firstBlock`, and write `+0x04` equal to `+0x00`.
- Let the last record own the last block: the block count that sizes the `+0x70` array comes from
  the last record alone, and a record owning a later block makes the load write past that array.
- Give a zero-size entry a `firstBlock` of 1 or more: the load reads the block-size entry at
  `firstBlock − 1` for it, which is out of bounds for 0. The shipped ones use 946,628 and up.
- Set `offset` to the absolute archive position of the entry's first stored block.
- Store each block as a zlib stream with its length in the block-size table, or raw: 0 for a full
  64 KiB block, or exactly `size & 0xFFFF` for an entry's last block. A compressed tail whose stream is
  exactly the tail's length would be read as raw, so store such a tail raw.
- Recompute the MD5 of `[0, indexSize)` into the last 16 bytes whenever the index changes. Replacing
  an entry's stored bytes in place with the same length leaves the index, and so the digest, unchanged.
- A mod can mount up to four more archives through `0x0019B070`; slots are searched in order, so an
  earlier slot overrides a later one.

## Related

- [How a path is resolved to bytes](file-path-resolution.md): the name normalisation and the two routes in front of the lookup.
- [Prefetch manifests](prefetch-manifests.md): the prefetch data in the archive.
