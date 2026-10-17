---
title: "Bigfile archive: the VBF container, how its index loads and is checked, and how a read reaches the file"
kind: "system"
category: "Game files and data tables"
addresses: "0017CEB0, 0019B070, 001F4340, 001F4120, 001F4720, 001F3FD0, 0019AEE0, 001F47D0, 001F4250, 00214FC0, 00215290, 00215110, 0019AFE0, 0019A770, 0019A860, 0019AA20, 0080C5A0, 01F81110, 009038C8, 008C2140, 008C2EF0, 0017D280, 008098D4, 007A0A80, 001F4060, 002150B0, 001F4840, 00215220, 0019B200, 0019A660, 0019A6E0, 0019A9B0"
---

## What the player sees

The game's data lives in one 31 GB file, `FFXII_TZA.vbf`, beside the game folder. It opens at once
at start-up, because only its index is read and checked; the data itself is read a piece at a time
as the game needs it. An edited index the game does not accept leaves the archive unmounted, and every
file the game then asks for fails to open. A compressed block that fails to inflate shows a Windows
error box, "Broken game data, please repair or restore the data."

## How it works

### Mounting

`0017CEB0` sets the base path (`0059A770("../../..")`), calls `0019B190`, and mounts
`"../FFXII_TZA.vbf"` into the archive manager from `0019B1F0` with `0019B070`; it never tests the
result. `0019B070(manager, path)` puts a new `B0`<sub>h</sub>-byte archive object in the first empty one of the
manager's five slots `+20h..+40h` and opens it with `001F4340`; when the open fails it destroys and
frees the object (`001F4120`) and clears the slot. With all five slots full it returns false without
opening anything. `0017CEB0` is the only caller of `0019B070`, so the shipped game fills slot 0 only.

`001F4060` constructs the object: an empty key tree whose
nodes come from a `PMapPair` allocator (`0067FFB0`, `30`<sub>h</sub>-byte nodes), null tables and handles, and the
critical section `+80`<sub>h</sub>.

### Loading and checking the index

`001F4340(archive, path)` copies the path into a 260-byte buffer (`+78`<sub>h</sub>) and opens it with CRT
`fopen(path, "rb")`; a null path or a failed `fopen` returns false. It reads the magic and refuses
anything but `4B595253`<sub>h</sub> (`'SRYK'`): it logs `"BigFile head wrong!\n"` (`009038C8`) through `0017D280`
and returns false without closing the file. It reads `indexSize` (the second dword), seeks 16 bytes
before the end and reads the stored digest there, then reads the first `indexSize` bytes of the file
in one `fread` into `+00`<sub>h</sub> and closes the file.

It hashes that buffer with MD5 (`CryptCreateHash`, `8003`<sub>h</sub>) and compares the two 64-bit halves with
the stored digest; on a mismatch it returns false with no message. None of the six CryptoAPI results
is tested; only the digest buffer is compared. The digest covers the header, keys, records, names and
block-size table, and nothing after `indexSize`: the payload lies outside the check.

### Parsing the index

After the check the opener:

1. Finds the record array after the keys, the name table after the records, and the block-size
   table after the names (`+68`<sub>h</sub>).
2. Computes the block count `+60`<sub>h</sub> from the last record: its first block plus `size >> 16`, plus one
   when `size & FFFFh` is non-zero.
3. Builds a one-byte-per-block array at `+70`<sub>h</sub>: 0 where the block-size entry is 0, otherwise 1; then,
   for each entry, its last block is set to 0 when the entry's block-size value equals
   `size & FFFFh`.
4. Rebases each record's `nameOffset` to a pointer (adding the name table's start) and inserts the
   record under its key into a red-black tree at `+08`<sub>h</sub> (`001F4720` → `001F3FD0`); nodes hold the key
   at `+18`<sub>h</sub> and the record pointer at `+28`<sub>h</sub>, ordered by the halves as signed 64-bit values, `+18`<sub>h</sub>
   first and `+20`<sub>h</sub> on a tie (`001F4008`-`001F4028`).
5. Allocates fifteen `30`<sub>h</sub>-byte reader handles (`2D8`<sub>h</sub> bytes, a count of 15 first) at `+A8`<sub>h</sub>, and
   opens the archive in each one (`00215290`).

### Finding a file

`0019AEE0(manager, name)` returns 0 when the manager pointer `01F81110` is null. Otherwise it
MD5-hashes the name from offset `[manager + 70h]` and asks each filled slot in order 0 to 4 through
`001F47D0(archive, digest)`; the first hit wins. `001F47D0` walks the tree with the same signed order
and hands the record to `001F4250`, which takes the first free handle of the fifteen under the
archive's lock (`+80`<sub>h</sub>). When all fifteen are busy it builds a fresh handle for that open
(`008098D4(30h)`, `00214FC0`, `00215290`), which never joins the pool. The lookup never compares
names.

`002150B0(handle, record)` binds a handle: it stores the record at `+18`<sub>h</sub>, sets the position `+20`<sub>h</sub>
and the window's bounds to 0 and the in-use byte `+00`<sub>h</sub> to 1. The resolver takes the file's size from
the record through `00215280`. Closing a stream releases its handle through `002150D0` →
`001F4840(archive, handle)`: a handle of the fifteen is cleared (`002152D0`: record, position and
in-use byte), and any other is destroyed (`00215040`: frees its 64 KiB window and closes its file) and
freed.

### Reading bytes

A handle read `00215110(handle, buffer, n)` takes n as 32 bits, clamps it to `size − position` when the read would pass the
entry's size (returning 0 when nothing is left), serves what it can from the handle's 64 KiB window,
and passes the rest to the archive reader `0019AFE0`.

A handle seek `00215220(handle, offset, origin)` sets the position to the offset (origin 0), adds
the offset (1) or sets it to the size minus the offset (2), and returns the new position, or
`FFFFFFFF` for another origin. It tests only the offset argument: a negative offset or one above the
size returns `FFFFFFFF` after the position has changed, and origin 1 can move the position past the
size.

`0019A770` plans a read: starting at the record's `firstBlock` and its archive `offset`, it skips
whole 64 KiB blocks by adding each skipped block's stored size (a block-size value of 0 counts as
`10000`<sub>h</sub>). `0019A860` seeks there (`_fseeki64`) and reads the stored blocks with CRT `fread`.
`0019AA20` turns each block into 64 KiB (or the tail's length): a block whose `+70`<sub>h</sub> byte is 0 is
copied as stored, any other is inflated with zlib 1.2.11's `uncompress` (`0080C5A0`).

When an
`uncompress` call returns an error or the total differs from the expected length `+58`<sub>h</sub>, it
loads string-table text `7834`<sub>h</sub> (`0019A510`, [Steam integration](../Steam-And-Achievements/steam-integration.md)),
shows it with `MessageBoxW` under the caption "error" and sets its state `+88`<sub>h</sub> to 6; otherwise
the state becomes 5.

`0019AA20` ORs every
`uncompress` result; when any is non-zero, or the bytes produced do not total the request (`+58`<sub>h</sub>),
it calls `007A0A80(1)`, shows `MessageBoxW` with string resource `7834`<sub>h</sub> and caption `error`, and
sets the read's state `+88`<sub>h</sub> to 6; otherwise to 5.

### Read records

The manager `01F81110` (`80`<sub>h</sub> bytes, `0019B190` → `0019AE70`) holds thirty read records of `98`<sub>h</sub>
bytes built by `0019B200(manager + 8, 30)`, which constructs each with `0019A3B0` (`0019A2A0`: three
part descriptors, each with its own 64 KiB buffer) and creates a semaphore with thirty counts.

- `0019A660` waits on the semaphore, then claims the first record whose busy word `+90`<sub>h</sub> it can
  change from 0 to 1 atomically, and raises its use count `+40`<sub>h</sub>.
- `0019A6E0(manager, start, block, n)`, `block` = `10000`<sub>h</sub>, takes a record that way. With `start`
  not 0 it marks the head used with offset `start` and length `head = min(block - start, n)`, then
  `n -= head` (`0019A70F`-`0019A736`); it marks the middle used when `n >= block`
  (`0019A739`-`0019A741`) and the tail used with length `n % block` when that is above 0
  (`0019A744`-`0019A759`).
- After the read, `0019A9B0` lowers the use count under the manager's critical section `+48`<sub>h</sub>; at 0
  it resets the record (`0019B130`), clears the busy word and releases one semaphore count.

`0019AFE0` returns the byte count it was asked for when the read's state is 5 and 0 otherwise.

The import table has no `CreateFileMapping` or `MapViewOfFile`. `ReadFile` (`008C2140`) has three
call sites (`0059A9B0`, `0059D4B0`, `0059F4A0`), `SetFilePointer` two and `CreateFileA` two (the
minidump writers `005CCAB0` and `0079B1E0`); CRT `fread` (`008C2EF0`) has 17, including
`001F4340` and `0019A860`.

## Layouts

### Index

The file starts with the index; `indexSize` bytes of it are covered by the digest.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u32` | magic | `'SRYK'` |
| `04`<sub>h</sub> | `u32` | indexSize | |
| `08`<sub>h</sub> | `u32` | count | entries |
| `0C`<sub>h</sub> | `u32` | zero | not read |
| `10`<sub>h</sub> | `u8[16]` | keys | one per entry: the MD5 of its name |

After the keys come `count` entry records, then the names (a `u32` length that counts itself, then
NUL-terminated lower-case names), then one `u16` block size per 64 KiB block up to `indexSize`: 0 for a full
raw block, `size & FFFFh` in an entry's last block for a raw tail, otherwise the length of a zlib stream.
The last 16 bytes of the file are the MD5 of `[0, indexSize)`.

### Entry record

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u32` | firstBlock | |
| `04`<sub>h</sub> | `u32` | firstBlock copy | not read |
| `08`<sub>h</sub> | `u64` | size | uncompressed |
| `10`<sub>h</sub> | `u64` | offset | archive offset of the first stored block |
| `18`<sub>h</sub> | `u64` | nameOffset | from the first name |

### Archive object

`B0`<sub>h</sub> bytes.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `void*` | index | |
| `08`<sub>h</sub> | `KeyTree` | keys | |
| `60`<sub>h</sub> | `u32` | block count | |
| `68`<sub>h</sub> | `u16*` | block sizes | |
| `70`<sub>h</sub> | `u8*` | compressed | one byte per block: 0 raw, 1 zlib |
| `78`<sub>h</sub> | `char*` | path | a 260-byte copy |
| `80`<sub>h</sub> | `CRITICAL_SECTION` | lock | |
| `A8`<sub>h</sub> | `ReaderHandle*` | handles | the fifteen reader handles |

### Reader handle

`30`<sub>h</sub> bytes.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u8` | in use | |
| `08`<sub>h</sub> | `FILE*` | file | |
| `10`<sub>h</sub> | `void*` | archive | |
| `18`<sub>h</sub> | `void*` | record | the entry record |
| `20`<sub>h</sub> | `u64` | position | |
| `28`<sub>h</sub> | `Window*` | window | a 64 KiB buffer, its end at `8` and its start at `10` |

### Read record

`98`<sub>h</sub> bytes, thirty of them.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `04`<sub>h</sub> | `u32` | block | the first block read |
| `08`<sub>h</sub> | `Part*` | head | |
| `10`<sub>h</sub> | `Part*` | middle | |
| `18`<sub>h</sub> | `Part*` | tail | |
| `30`<sub>h</sub> | `u32` | owned | non-zero: the reset frees the buffer at `38`; zeroed by `0019A2A0` and the reset `0019B130` |
| `38`<sub>h</sub> | `void*` | buffer | freed with `free` while `30` is non-zero |
| `40`<sub>h</sub> | `u32` | use count | |
| `48`<sub>h</sub> | `u64` | archive offset | |
| `50`<sub>h</sub> | `u64` | skipped | bytes in whole blocks skipped |
| `58`<sub>h</sub> | `u32` | length | the request |
| `88`<sub>h</sub> | `u32` | state | `5` done, `6` failed |
| `90`<sub>h</sub> | `u32` | busy | |

### Part

`18`<sub>h</sub> bytes.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u8` | used | |
| `08`<sub>h</sub> | `u8*` | buffer | 64 KiB |
| `10`<sub>h</sub> | `u32` | length | |
| `14`<sub>h</sub> | `u32` | offset | within the block |

The reader's own records and banks are listed field by field in
[`bigfile-archive-slow-reader-manager-accesses.tsv`](bigfile-archive-slow-reader-manager-accesses.tsv),
[`bigfile-archive-slow-reader-record-bank-accesses.tsv`](bigfile-archive-slow-reader-record-bank-accesses.tsv),
[`bigfile-archive-slow-reader-record-accesses.tsv`](bigfile-archive-slow-reader-record-accesses.tsv) and
[`bigfile-archive-slow-reader-block-descriptor-accesses.tsv`](bigfile-archive-slow-reader-block-descriptor-accesses.tsv).

## Shipped data

| Fact | Value |
|---|---|
| file size | 31,196,932,183 bytes |
| error text | string `7834`<sub>h</sub> in nine languages; English "Broken game data, please repair or restore the data." |
| `indexSize` | 11,995,716 bytes; MD5 matches the last 16 bytes |
| entries | 89,414; 89,388 with bytes and 26 of size 0 (`jsondata/cutscenes/*.json`) |
| keys | all 89,414 equal the MD5 of their entry's name; every name is lower case |
| `+04`<sub>h</sub> | equals `+00`<sub>h</sub> in all 89,388 entries with bytes |
| offsets | each entry starts where the one before it ends, from `indexSize` to 16 bytes before the end |
| blocks | 957,553 (the last entry's first block plus its block count); 189,861 full raw blocks; 1,697 entries end in a raw tail |
| top folders | `gamedata` 39,653, `ps2data` 39,578, `prefetchdata` 9,351, `jsondata` 832 |
| extensions | `.phyre` 35,984, `.txt` 10,253, `.ebp` 10,045, `.sab` 4,609, `.mot` 4,392, `.efx` 3,288, `.ca` 3,164, `.dat` 2,948, `.ah` 2,564, `.snd` 2,304 |

## Operations

At start-up: one 12 MB read, one MD5 over it and one tree insert per entry. Per file open: one MD5 of
the path, one tree walk per mounted archive and one handle. Per read: one seek and one `fread` per
stored block, and one inflate per compressed block.

## State

The archive manager at `01F81110` with its five slots; each archive's index buffer, key tree, block
tables and reader handles.

## Modding notes

To repack `FFXII_TZA.vbf` so that the game accepts it:

- Give every entry a key equal to the MD5 of its lower-case name with forward slashes.
- Keep an entry's blocks consecutive from `firstBlock`, and write `+04`<sub>h</sub> equal to `+00`<sub>h</sub>.
- Let the last record own the last block: the block count that sizes the `+70`<sub>h</sub> array comes from
  the last record alone, and a record owning a later block makes the load write past that array.
- Give a zero-size entry a `firstBlock` of 1 or more: the load reads the block-size entry at
  `firstBlock − 1` for it, which is out of bounds for 0. The shipped ones use 946,628 and up.
- Set `offset` to the absolute archive position of the entry's first stored block.
- Store each block as a zlib stream with its length in the block-size table, or raw: 0 for a full
  64 KiB block, or exactly `size & FFFFh` for an entry's last block. A compressed tail whose stream is
  exactly the tail's length would be read as raw, so store such a tail raw.
- Recompute the MD5 of `[0, indexSize)` into the last 16 bytes whenever the index changes. Replacing
  an entry's stored bytes in place with the same length leaves the index, and so the digest, unchanged.
- A mod can mount up to four more archives through `0019B070`; slots are searched in order, so an
  earlier slot overrides a later one.

## Related

- [How a path is resolved to bytes](file-path-resolution.md): the name normalisation and the two routes in front of the lookup.
- [Prefetch manifests](prefetch-manifests.md): the prefetch data in the archive.
