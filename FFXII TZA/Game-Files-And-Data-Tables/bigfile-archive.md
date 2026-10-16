---
title: "Bigfile archive: the VBF container, how its index loads and is checked, and how a read reaches the file"
kind: "system"
category: "Game files and data tables"
summary: "The FFXII_TZA.vbf archive the game reads its data from: how it is mounted, the SRYK header, the index of MD5 keys, 32-byte entry records, names and the 64 KiB block-size table, the MD5 check over the index and what it does not cover, the lookup by the MD5 of a path, the pool of reader handles and how one is bound, sought and released, the thirty read records, how a read is planned block by block and inflated with zlib, the shipped counts, and the rules a repacker must follow."
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
result. `0019B070(manager, path)` puts a new `0xB0`-byte archive object in the first empty one of the
manager's five slots `+0x20..+0x40` and opens it with `001F4340`; when the open fails it destroys and
frees the object (`001F4120`) and clears the slot. With all five slots full it returns false without
opening anything. `0017CEB0` is the only caller of `0019B070`, so the shipped game fills slot 0 only.

`001F4060` constructs the object: an empty key tree whose
nodes come from a `PMapPair` allocator (`0067FFB0`, `0x30`-byte nodes), null tables and handles, and the
critical section `+0x80`.

### Loading and checking the index

`001F4340(archive, path)` copies the path into a 260-byte buffer (`+0x78`) and opens it with CRT
`fopen(path, "rb")`; a null path or a failed `fopen` returns false. It reads the magic and refuses
anything but `0x4B595253` (`'SRYK'`): it logs `"BigFile head wrong!\n"` (`009038C8`) through `0017D280`
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
   record under its key into a red-black tree at `+0x08` (`001F4720` → `001F3FD0`); nodes hold the key
   at `+0x18` and the record pointer at `+0x28`, ordered by the two halves as signed 64-bit values.
5. Allocates fifteen `0x30`-byte reader handles (`0x2D8` bytes, a count of 15 first) at `+0xA8`, and
   opens the archive in each one (`00215290`).

### Finding a file

`0019AEE0(manager, name)` returns 0 when the manager pointer `01F81110` is null. Otherwise it
MD5-hashes the name from offset `[manager + 0x70]` and asks each filled slot in order 0 to 4 through
`001F47D0(archive, digest)`; the first hit wins. `001F47D0` walks the tree with the same signed order
and hands the record to `001F4250`, which takes the first free handle of the fifteen under the
archive's lock (`+0x80`). When all fifteen are busy it builds a fresh handle for that open
(`008098D4(0x30)`, `00214FC0`, `00215290`), which never joins the pool. The lookup never compares
names.

`002150B0(handle, record)` binds a handle: it stores the record at `+0x18`, sets the position `+0x20`
and the window's bounds to 0 and the in-use byte `+0x00` to 1. The resolver takes the file's size from
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
`0x10000`). `0019A860` seeks there (`_fseeki64`) and reads the stored blocks with CRT `fread`.
`0019AA20` turns each block into 64 KiB (or the tail's length): a block whose `+0x70` byte is 0 is
copied as stored, any other is inflated with zlib 1.2.11's `uncompress` (`0080C5A0`).

`0019AA20` ORs every
`uncompress` result; when any is non-zero, or the bytes produced do not total the request (`+0x58`),
it calls `007A0A80(1)`, shows `MessageBoxW` with string resource `0x7834` and caption `error`, and
sets the read's state `+0x88` to 6; otherwise to 5.

### Read records

The manager `01F81110` (`0x80` bytes, `0019B190` → `0019AE70`) holds thirty read records of `0x98`
bytes built by `0019B200(manager + 8, 30)`, which constructs each with `0019A3B0` (`0019A2A0`: three
part descriptors, each with its own 64 KiB buffer) and creates a semaphore with thirty counts.

- `0019A660` waits on the semaphore, then claims the first record whose busy word `+0x90` it can
  change from 0 to 1 atomically, and raises its use count `+0x40`.
- `0019A6E0(manager, start, 0x10000, n)` takes a record that way and divides the n bytes from `start`
  within the first block into a head (the rest of that block, when `start` is not 0), a middle (used
  when at least one whole block remains) and a tail (the remainder), marking each part used.
- After the read, `0019A9B0` lowers the use count under the manager's critical section `+0x48`; at 0
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
| `00` | `u32` | magic | `'SRYK'` |
| `04` | `u32` | indexSize | |
| `08` | `u32` | count | entries |
| `0C` | `u32` | zero | not read |
| `10` | `u8[16]` | keys | one per entry: the MD5 of its name |

After the keys come `count` entry records, then the names (a `u32` length that counts itself, then
NUL-terminated lower-case names), then one `u16` block size per 64 KiB block up to `indexSize`: 0 for a full
raw block, `size & 0xFFFF` in an entry's last block for a raw tail, otherwise the length of a zlib stream.
The last 16 bytes of the file are the MD5 of `[0, indexSize)`.

### Entry record

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u32` | firstBlock | |
| `04` | `u32` | firstBlock copy | not read |
| `08` | `u64` | size | uncompressed |
| `10` | `u64` | offset | archive offset of the first stored block |
| `18` | `u64` | nameOffset | from the first name |

### Archive object

`0xB0` bytes.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `void*` | index | |
| `08` | `KeyTree` | keys | |
| `60` | `u32` | block count | |
| `68` | `u16*` | block sizes | |
| `70` | `u8*` | compressed | one byte per block: 0 raw, 1 zlib |
| `78` | `char*` | path | a 260-byte copy |
| `80` | `CRITICAL_SECTION` | lock | |
| `A8` | `ReaderHandle*` | handles | the fifteen reader handles |

### Reader handle

`0x30` bytes.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u8` | in use | |
| `08` | `FILE*` | file | |
| `10` | `void*` | archive | |
| `18` | `void*` | record | the entry record |
| `20` | `u64` | position | |
| `28` | `Window*` | window | a 64 KiB buffer, its end at `8` and its start at `10` |

### Read record

`0x98` bytes, thirty of them.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `04` | `u32` | block | the first block read |
| `08` | `Part*` | head | |
| `10` | `Part*` | middle | |
| `18` | `Part*` | tail | |
| `40` | `u32` | use count | |
| `48` | `u64` | archive offset | |
| `50` | `u64` | skipped | bytes in whole blocks skipped |
| `58` | `u32` | length | the request |
| `88` | `u32` | state | `5` done, `6` failed |
| `90` | `u32` | busy | |

### Part

`0x18` bytes.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u8` | used | |
| `08` | `u8*` | buffer | 64 KiB |
| `10` | `u32` | length | |
| `14` | `u32` | offset | within the block |

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

The archive manager at `01F81110` with its five slots; each archive's index buffer, key tree, block
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
- A mod can mount up to four more archives through `0019B070`; slots are searched in order, so an
  earlier slot overrides a later one.

## Related

- [How a path is resolved to bytes](file-path-resolution.md): the name normalisation and the two routes in front of the lookup.
- [Prefetch manifests](prefetch-manifests.md): the prefetch data in the archive.
