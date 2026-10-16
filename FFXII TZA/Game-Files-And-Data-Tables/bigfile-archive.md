---
title: "Bigfile archive: the VBF container, how its index loads and is checked, and how a read reaches the file"
kind: "system"
category: "Game files and data tables"
summary: "The FFXII_TZA.vbf archive the game reads its data from: how it is mounted, the SRYK header, the index of MD5 keys, 32-byte entry records, names and the 64 KiB block-size table, the MD5 check over the index and what it does not cover, the lookup by the MD5 of a path, the pool of reader handles, how a read is planned block by block and inflated with zlib, the shipped counts, and the rules a repacker must follow."
addresses: ["0017CEB0", "0019B070", "001F4340", "001F4120", "001F4720", "001F3FD0", "0019AEE0", "001F47D0", "001F4250", "00214FC0", "00215290", "00215110", "0019AFE0", "0019A770", "0019A860", "0019AA20", "0080C5A0", "01F81110", "009038C8", "008C2140", "008C2EF0", "0017D280", "008098D4", "007A0A80"]
---

# Bigfile archive: the VBF container, how its index loads and is checked, and how a read reaches the file

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

### Reading bytes

A handle read `00215110(handle, buffer, n)` takes n as 32 bits, clamps it to `size − position` when the read would pass the
entry's size (returning 0 when nothing is left), serves what it can from the handle's 64 KiB window,
and passes the rest to the archive reader `0019AFE0`.

`0019A770` plans a read: starting at the record's `firstBlock` and its archive `offset`, it skips
whole 64 KiB blocks by adding each skipped block's stored size (a block-size value of 0 counts as
`0x10000`). `0019A860` seeks there (`_fseeki64`) and reads the stored blocks with CRT `fread`.
`0019AA20` turns each block into 64 KiB (or the tail's length): a block whose `+0x70` byte is 0 is
copied as stored, any other is inflated with zlib 1.2.11's `uncompress` (`0080C5A0`).

`0019AA20` ORs every
`uncompress` result; when any is non-zero, or the bytes produced do not total the request (`+0x58`),
it calls `007A0A80(1)`, shows `MessageBoxW` with string resource `0x7834` and caption `error`, and
sets the read's state `+0x88` to 6; otherwise to 5.

The import table has no `CreateFileMapping` or `MapViewOfFile`. `ReadFile` (`008C2140`) has three
call sites (`0059A9B0`, `0059D4B0`, `0059F4A0`), `SetFilePointer` two and `CreateFileA` two (the
minidump writers `005CCAB0` and `0079B1E0`); CRT `fread` (`008C2EF0`) has 17, including
`001F4340` and `0019A860`.

## Layouts

```
index header  +0x00 u32 magic 'SRYK', +0x04 u32 indexSize, +0x08 u32 count, +0x0C u32 zero (not read)
keys          +0x10: count x 16 bytes, key i = MD5 of entry i's name
records       after the keys: count x 0x20
  +0x00 u32 firstBlock, +0x04 u32 copy of +0x00 (not read), +0x08 u64 size (uncompressed),
  +0x10 u64 offset (archive offset of the first stored block), +0x18 u64 nameOffset (from the first name)
names         after the records: u32 length (counting itself), then NUL-terminated lower-case names
block sizes   to indexSize: u16 per 64 KiB block; 0 = full raw block, size & 0xFFFF in a last block = raw tail,
              otherwise the length of a zlib stream
digest        the last 16 bytes of the file: MD5 of [0, indexSize)
archive obj   0xB0: +0x00 index, +0x08 key tree, +0x60 block count, +0x68 block sizes, +0x70 raw/zlib bytes,
              +0x78 path, +0x80 lock, +0xA8 reader handles
```

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
