---
title: "File path resolution: how a file name becomes bytes through the RAM file cache or the archive, the stream reader, and what lives under .dat and .bin"
kind: "system"
category: "Game files and data tables"
addresses: "0x00597970, 0x00597930, 0x0059EE90, 0x0059D920, 0x0059D4B0, 0x0059BD40, 0x0059FDA0, 0x0059FD10, 0x0059ED70, 0x00D26C60, 0x00D26C90, 0x001D6B20, 0x001D6B90, 0x001D6B70, 0x00865390, 0x001DB050, 0x01F83440, 0x01F83441, 0x001D6D20, 0x0020C1B0, 0x0020C440, 0x00674A00, 0x0020C300, 0x00217A60, 0x00217A70, 0x00217AD0, 0x0019AEE0, 0x0059A9B0, 0x001D6BB0, 0x0020BFA0, 0x0020B130, 0x001D6A20, 0x0020B680, 0x0020B5F0, 0x0020B0F0, 0x0020B840, 0x001D6AA0, 0x0020B9A0, 0x00599250, 0x00D27930, 0x00D27910, 0x00D27948, 0x00597A20, 0x00597A70, 0x0059BD80, 0x0059D900, 0x0059FBA0, 0x0059D510, 0x0020C150, 0x0020B0D0, 0x0020B150, 0x0020C560"
---

## What the player sees

Every model, texture, script or table the game opens by name goes through this path. A file the game
has read before may come from a RAM cache; otherwise it is read from `FFXII_TZA.vbf`. There are no
loose files on disk to fall back to: a name the archive does not hold logs
`[FFXII_ERROR] Big file open failed` and that asset does not load. In play this shows only as load
time.

## How it works

### The stream

`0x00597970(stream, name, selector)` constructs a `Phyre::PSerialization::PStreamReaderFile` (vtable
`0x00D26C90`, over the abstract `PStream` at `0x00D26C60`). It sets the Win32 handle `+0x28` to −1, the
archive reader `+0x30` to 0, the cache view `+0x40` to −1, the key `+0x48` to 0 and the selector byte
`+0x38`, and, for a non-null name, runs the resolver `0x0059EE90(stream + 0x20, name, 1)`. It keeps a
copy of the name at `+0x10` (`0x001C26B0`) and the size the resolver found at `+0x20`. The constructor
ignores the resolver's status. `0x00597930` builds the same `0x30`-byte frame without the stream.

| Slot | Body | What it does |
|---|---|---|
| 0 | `0x00598280` | destructor |
| 1 | `0x0059BD40` | Close: releases the archive reader (`0x002150D0`) and zeroes `+0x30`; when `+0x40` is positive, releases the view (`0x001D6AA0(key, view)`) and sets `+0x40` to −1; returns 1; never touches `+0x28` |
| 2 | `0x0059D920` | IsOpen: false only when `+0x28` = −1, `+0x30` = 0 and `+0x40` = −1 |
| 3 | `0x0059ED70` | Rebind: resolves a new name and replaces the copy |
| 4 | `0x0059FAC0` | Close, then Rebind |
| 5 | `0x0059D4B0` | Read: through the archive reader when `+0x30` is set (`0x002150E0`); a zero count returns 0; else `ReadFile` on `+0x28`, returning the bytes read; else the view when `+0x40` is positive (`0x001D6CA0`); else 0 |
| 6 | `0x0059FDA0` | Seek relative (origin 1) through the archive reader, the Win32 handle (`SetFilePointer`) or the view, the first that is set; returns the requested offset, or 0 when the backend reports −1 |

The low bit of the name pointer at `+0x10` marks a borrowed string: Rebind, Close-then-Rebind and the
base destructor `0x00598100` free the copy only when that bit is clear. `0x00598140`, the `PStream` base
destructor, reinstalls that vtable and frees an owned name the same way.

### Other constructors and frame helpers

- `0x00597A20` builds a `PStreamReaderFile` with no name: handle −1, view −1, no archive reader, and
  selector 1.
- `0x00597A70(stream, name)` builds a `PStreamWriterFile` (over `PStream`) with selector 0; it runs the
  resolver on the name with `cacheable` 0 and keeps a copy of the name.
- `0x0059BD80(frame)` and `0x0059D900(frame)` are Close and IsOpen on the `+0x20` frame alone, for code
  that holds a frame without its stream; `0x001D6E80(frame)` closes one and frees it.
- `0x0059FBA0(frame, offset, origin)` seeks with an origin: through the archive reader (`0x00215220`),
  `SetFilePointer`, or a positive view (`0x0020C180` → `0x00217AD0`), the first that is set, and returns
  −1 when none is.
- `0x0019EAA0(…, name)` opens a name (selector 1), closes it when it opened, and returns whether it did.
- `0x0059D510(stream, buffer, n)` reads through slot 5, adds the count to the stream's dword `+0x18`,
  and returns 0 when all n bytes came and 9 otherwise.

### The resolver

`0x0059EE90(frame, name, cacheable)`:

1. When the byte `0x01F83440` is set (`0x001D6B20`) and the name starts with
   `PS2Data\obj_finish\in\chara\c10\` followed by `c1004`, `c1005`, `c1006` or `c1019` and a
   backslash (`0x00865390` → `0x001DB050`, a case-sensitive prefix compare), the selector becomes 5.
2. Selectors 3, 4 and 5 log nothing; selector 0 logs `[FFXII_data_notcache] %s`; any other selector
   logs `[FFXII_data] %s` (`0x00D27910`, `0x00D27930`).
3. Route 1, the RAM cache, is tried when `0x01F83440` is set, the selector is non-zero, `cacheable`
   is set and the name passes the filter below. A view of 0 or more is a hit: the size goes to the
   frame and the resolver returns 0.
4. Otherwise route 2, the archive: the name is copied with one leading `/` or `\` dropped, a
   lower-case backslash copy is converted to UTF-16 (`0x00599250`) and not used further, and a second
   copy skips every leading `.`, `/` or `\`, turns `\` into `/` and lower-cases `A`-`Z`. That copy is
   looked up in the archive (`0x0019AEE0`).
5. A miss logs `[FFXII_ERROR] Big file open failed %s` (`0x00D27948`) and returns 10. A hit stores the
   reader at frame `+0x10` and the size, copies the file into the cache when the backfill flag below is
   set, and returns 0.

The backfill flag is set on a route-1 miss when the byte
`0x01F83441` (`0x001D6B90`) is 0 or the selector is 5, and then when `0x001D6B70` (byte `+0x88` of `0x001DADA0()`) is set or the
selector is not 1. The flag is computed only on the route-1 path, and the key the backfill files
under is the one route 1 stored, so a name that fails the filter, or is opened with selector 0 or
without `cacheable`, is never copied into the cache.

### The name filter

Route 1 is skipped for a name of 3 characters or fewer, or 4 or fewer, and when any one of these
characters matches, each tested on its own: the 4th from the end is `.`, the 3rd is `m`, the 2nd is
`a`, the last is `b`; the 5th from the end is `.`, the 4th is `w`, the 3rd is `e`, the 2nd is `b`, the
last is `m`. The tests aim at `.mab` and `.webm`, but they also send to the archive every name with a
three- or four-character extension and every name ending in `b` or `m`.

### Route 1: the RAM file cache

`0x001D6D20` takes the cache manager (`0x0020C700`) and calls `0x0020C1B0(manager, name, selector, &size,
&key)`:

- `0x0020C440` builds the key: it skips leading characters until the first letter or digit, turns `/`
  into `\`, copies through CRT `toupper` while dropping the first of two adjacent backslashes, and
  strips trailing spaces.
- An empty key returns −1. Otherwise the key is hashed with `0x00674A00` (seed `0x1505`,
  `hash × 33 + (signed char)c`, bit 31 cleared) and the hash is stored through the key pointer before
  the search.
- Under the manager's lock (`+0x58`), the tree rooted at `+0x38` (header `+0x28`) is searched with
  unsigned compares on each node's dword `+0x20`. A miss returns −1.
- A hit writes the entry's size, then `0x0020C300` builds the view.

`0x0020C300(manager, key, data, size, selector, kind)` adds one to the manager's `+0x88` and to the
entry's byte `+0x10`, then stamps the entry:

- selector 5 and kind 1 to 4: kind `+0x14` becomes 5;
- otherwise kind 5 or selector 5: no stamp;
- otherwise selector 3: word `+0x0E` takes the word at `[manager + 0x18] + 0xE8`;
- otherwise selector 1, 2 or 4: word `+0x0C` takes the manager's word `+0x80`.

It then allocates a 16-byte view `{data, size, position 0}` (`0x00217A60`). When that allocation fails
it returns 0, which the resolver takes as a hit: the stream is left with no readable backing, IsOpen
true, and every Read returning 0.

### Reading a cache view

A view read `0x00217A70(view, buffer, n)` returns `FFFFFFFF` for a null buffer. It computes
`position + n` as a 32-bit sum and, when that exceeds the size, takes `size − position` instead; it
copies that many bytes from `data + position` and advances the position. A wrapped sum keeps the full
request. A view seek `0x00217AD0(view, offset, origin)` sets the position to the offset (origin 0), the
position plus the offset (1) or the size plus the offset (2), leaves it for any other origin, and then
clamps it to the size; there is no lower clamp.

Releasing a view, `0x0020B9A0(manager, key, view)`, takes the lock, finds the entry by key and lowers its
byte `+0x10` by one unless it is 0, and then frees the 16-byte view whether or not the key was found.
The cached bytes stay in the cache.

`0x0020C150(cache, view, buffer, n)` is the read that slot 5 reaches through `0x001D6CA0`: it calls
`0x00217A70` when the view and the count are both non-zero and returns 0 otherwise.

### Copying an archive hit into the cache

`0x0059A9B0(frame, key)` asks the cache for a buffer of the file's size (`0x001D6BB0` → `0x0020BFA0(cache,
size, selector ≠ 1)`), reads the whole file into it from the archive reader (or the Win32 handle, or a
view), logs `read bytes count is not same as file size (%08x)!` on a short read, closes the archive
reader and the Win32 handle, and inserts the buffer under the key with the selector as its kind
(`0x001D6A20` → `0x0020B680`). The view the insertion returns becomes the stream's `+0x40`, so later reads
come from the cache; a result of 0 or less frees the buffer again.

`0x0020B680(cache, key, &buffer, size, kind)`:

- **New key.** It adds a descriptor `{data +0, size +8, word +0x0C, word +0x0E, byte +0x10 = 1,
  kind +0x14}` under the key (`0x0020B5F0`). Kind 5 gets `+0x0C` = 0; kind 3 gets `+0x0E` from
  `[cache + 0x18] + 0xE8`; any other kind gets `+0x0C` from the cache's word `+0x80` and `+0x0E` =
  −1. It returns a new view and adds the size to the cache's byte total `+0x90`.
- **Key already present.** It frees the incoming buffer (`0x0020B0F0`) and returns a view of the
  existing entry through `0x0020C300`.

### The cache's memory budget and eviction

The constructor's first step, `0x0020B0D0`, stores the limit at `+0x00`, `0x10000` in the dword `+0x08`
and 0 as the usage. Cache entries come from a record pool at `+0x98` (`0x0020B150`, built without a
lock of its own; `0x0020B3E0` destroys it); `0x0020C560` sizes its vector, and `0x0020BB10` fills new records
with `{data 0, size 0, +0x0C 0, +0x0E −1, views 0, kind 1}`.


`0x0020B130(cache, size)` refuses an allocation when the usage `+0x10` is above the limit `+0x00`;
otherwise it adds the size to the usage and calls `malloc`. The test runs before the size is added,
so one allocation can take the usage past the limit by its whole size. `0x0020B0F0` subtracts the block's `_msize`
from the usage and frees it.

When the allocation fails, `0x0020BFA0` frees unprotected entries, oldest first from the list at
`+0x30`, until `max(200,000,000, 3 × size)` bytes are released; each freed entry leaves the byte total,
the map at `+0x98` and the count `+0x48`. An entry is protected when:

- its byte `+0x10` is non-zero or its kind is 5;
- its word `+0x0E` is not negative and equals `[[cache + 0x18] + 0xE8]`;
- its word `+0x0C` is positive and equals the cache's `+0x80` or `+0x84`.

When the list runs out it calls `0x0020B840(cache, remaining, 1, 0)` and retries. `0x0020B840` applies the
same tests (the `+0x0E` and `+0x0C` ones only while its fourth argument is 0, the `+0x84` one only
while its third is 0), walks twice when the first pass falls short, and returns whether the walk
reached the end of the list.

## Layouts

```python
stream          +0x10 name copy (bit 0 = borrowed), +0x20 frame: +0x20 u32 size, +0x28 Win32 handle (-1),
                +0x30 archive reader (0), +0x38 u8 selector, +0x40 cache view (-1), +0x48 u32 cache key
cache entry     +0x00 data, +0x08 u32 size, +0x0C s16, +0x0E s16, +0x10 u8 views open, +0x14 u32 kind
cache view      +0x00 data, +0x08 u32 size, +0x0C u32 position
cache manager   +0x00 limit, +0x10 usage, +0x18 owner (+0xE8 word), +0x20 key map (header +0x28, root +0x38),
                +0x30 entry list, +0x48 count, +0x58 lock, +0x80 / +0x84 protected words, +0x88 hits, +0x90 bytes, +0x98 map
```

| | Route 1 (cache) | Route 2 (archive) |
|---|---|---|
| separator | `\` | `/` |
| case | upper, CRT `toupper` | lower, `A`-`Z` only |
| leading text | skipped to the first letter or digit | `.`, `/`, `\` skipped |
| other | doubled `\` collapsed, trailing spaces stripped | none |
| hash | 33-multiplicative, 31 bits | MD5, 128 bits |

## Shipped data

`.dat` and `.bin` name no single format; the leading four bytes of every shipped entry under them:

| Extension | Entries | Bytes | Signatures |
|---|---:|---:|---|
| `.dat` | 2,948 | 2,033,994,956 | `himg` 2,721, `hdat` 101, `hchk` 54, `qstd` 9, and 63 font tables with a small count as their first dword (17 values) |
| `.bin` | 1,439 | 2,481,360,070 | 59 signatures; `sloc` 436, `st2e` 407, zero dword 73, `hctg` 54, `licd` 52, `0x40` 42, `gmap` 35, then `FLAG`, `CCdd`, `CHSE`, `NPC0`, `PLMN`, `QST1`, `amap`, `cmap`, `lmap`, `wmap`, `hcom`, `hodr`, `sign` and headerless images among the rest |

The formats behind them are on the
[handbook image bundles](handbook-files.md),
[handbook indexes](handbook-files.md),
[menu map container](menu-map-files.md),
[character SE tables](character-se-tables-chse.md) and
[loader-bound bin families](ps2data-bin-families.md) pages.

## Operations

Per open: one key build and tree search when route 1 applies, otherwise two string copies, one MD5 and
one archive lookup; a backfill reads the whole file once more into the cache.

## State

The cache manager (its tree, entry list, byte totals, limit, usage and protected words), the two cache
flags `0x01F83440` and `0x01F83441`, and each open stream's backing fields.

## Modding notes

- A replacement file has to be in `FFXII_TZA.vbf` under the MD5 of its lower-case, forward-slash
  name; the RAM cache is filled only from archive hits during a run, so it adds no second place to put
  a file.
- Any hook on file access has to act at or above `0x0059EE90`.
- The name filter keeps names with a three- or four-character extension (`.ebp`, `.dat`, `.bin`,
  `.txt` and the like) and names ending in `b` or `m` out of the cache; `.phyre` files, the largest
  group, pass it.

## Related

- [Bigfile archive](bigfile-archive.md): the archive lookup, its reader handles and the block reads.
- [Prefetch manifests](prefetch-manifests.md): the token loop that resolves names with selector 5.
- [Texture animation lists](texture-animation-lists-ta.md): the same 33-multiplicative hash.
