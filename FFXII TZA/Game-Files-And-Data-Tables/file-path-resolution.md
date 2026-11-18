[Home](../../README.md) / [Game files and data tables](README.md) / File path resolution

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| File path resolution: how a file name becomes bytes through the RAM file cache or the archive, the stream reader, and what lives under .dat and .bin | system | Game files and data tables | Archives and file loading | How the game opens a file by name: the PStreamReaderFile stream and its read, seek, open and close slots, the resolver with its selector and log tags, route 1 into the RAM file cache (the upper-case key, the 33-multiplicative hash, the name filter, hits, stamps and views) and route 2 into the archive (the lower-case key and MD5), how an archive hit is copied into the cache, the cache's memory budget, insertion, eviction and view release, and the formats that share the .dat and .bin extensions. | 0x00597970, 0x00597930, 0x0059EE90, 0x0059D920, 0x0059D4B0, 0x0059BD40, 0x0059FDA0, 0x0059FD10, 0x0059ED70, 0x00D26C60, 0x00D26C90, 0x001D6B20, 0x001D6B90, 0x001D6B70, 0x00865390, 0x001DB050, 0x01F83440, 0x01F83441, 0x001D6D20, 0x0020C1B0, 0x0020C440, 0x00674A00, 0x0020C300, 0x00217A60, 0x00217A70, 0x00217AD0, 0x0019AEE0, 0x0059A9B0, 0x001D6BB0, 0x0020BFA0, 0x0020B130, 0x001D6A20, 0x0020B680, 0x0020B5F0, 0x0020B0F0, 0x0020B840, 0x001D6AA0, 0x0020B9A0, 0x00599250, 0x00D27930, 0x00D27910, 0x00D27948, 0x00597A20, 0x00597A70, 0x0059BD80, 0x0059D900, 0x0059FBA0, 0x0059D510, 0x0020C150, 0x0020B0D0, 0x0020B150, 0x0020C560 |

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
ignores the resolver's status.

The size starts at 0 (`0x0059798E`). After the resolver the constructor stores `0xB` in the dword `+0x08`
(`0x005979C2`), 0 in the dword `+0x18`, and in the dword `+0x1C` the size, or −1 when the size is 0
(`0x005979E9`-`0x00597A06`).

`0x00597930` builds the same `0x30`-byte frame without the stream. Its arguments are the frame, the name,
`cacheable` and the selector: it sets size 0, handle −1, no archive reader, view −1, key 0 and the
selector byte `+0x18` (`0x00597938`-`0x00597954`), runs the resolver with the caller's `cacheable` only for
a non-null name (`0x0059795D`), copies no name and returns the frame.

| Slot | Body | What it does |
|---|---|---|
| 0 | `0x00598280` | destructor |
| 1 | `0x0059BD40` | Close: releases the archive reader (`0x002150D0`) and zeroes `+0x30`; when `+0x40` is positive, releases the view (`0x001D6AA0(key, view)`) and sets `+0x40` to −1; returns 1; never touches `+0x28` |
| 2 | `0x0059D920` | IsOpen: false only when `+0x28` = −1, `+0x30` = 0 and `+0x40` = −1 |
| 3 | `0x0059ED70` | Rebind: resolves a new name and replaces the copy. It runs `0x0059EE90(stream + 0x20, name, 1)` for every name, a null one included, for which the resolver returns 1 (`0x0059EECC`), and stores the status in the dword `+0x08` (`0x0059ED9F`), where the constructor stores `0xB` (`0x005979C2`). The copy (`0x001C26B0`, null for a null name) replaces `+0x10` after an owned old copy is freed (`0x00584730`); a non-null name whose copy comes back null keeps the old copy (`0x0059EDB4`). It then zeroes the dword `+0x18` (`0x0059EDF0`), sets the dword `+0x1C` to the frame's dword `+0x20`, or −1 when that is 0 (`0x0059EDED`), and returns 1 when the resolver returned 0, else 0 (`0x0059EE02`) |
| 4 | `0x0059FAC0` | Close, then Rebind |
| 5 | `0x0059D4B0` | Read: through the archive reader when `+0x30` is set (`0x002150E0`), returning that call's result (`0x0059D4C0`); a zero count returns 0 (`0x0059D4D1`); else `ReadFile` on `+0x28` with a null `OVERLAPPED` pointer, returning the bytes read from a count that starts at 0, and the call's own success flag is dropped (`0x0059D4CA`, `0x0059D4EA`, `0x0059D4F0`); else the view when `+0x40` is positive (`0x001D6CA0`), returning that call's result (`0x0059D502`); else 0 |
| 6 | `0x0059FDA0` | Seek relative (origin 1) through the archive reader, the Win32 handle (`SetFilePointer`) or the view, the first that is set; returns the requested offset, or 0 when the backend reports −1. The slot moves to the `+0x20` frame and jumps to `0x0059FD10(frame, offset)`, which does the work: the archive reader at frame `+0x10` (`0x00215220`), else the handle at frame `+0x08` when it is not −1 (`SetFilePointer` with a null high part), else the view at frame `+0x20` when it is positive (`0x001D6CE0`); with no route set it also returns 0 (`0x0059FD7A`, `0x0059FD8A`) |

The low bit of the name pointer at `+0x10` marks a borrowed string: Rebind, Close-then-Rebind and the
base destructor `0x00598100` free the copy only when that bit is clear. `0x00598140`, the `PStream` base
destructor, reinstalls that vtable and frees an owned name the same way.

### Other constructors and frame helpers

- `0x00597A20` builds a `PStreamReaderFile` with no name: handle −1, view −1, no archive reader, and
  selector 1. It also sets size 0, key 0 and a null name, stores `0xB` in `+0x08`, 0 in `+0x18` and −1 in
  `+0x1C` (`0x00597A2A`-`0x00597A5B`), and returns the stream.
- `0x00597A70(stream, name)` builds a `PStreamWriterFile` (over `PStream`) with selector 0; it runs the
  resolver on the name with `cacheable` 0 and keeps a copy of the name. The resolver runs only for a
  non-null name (`0x00597AA9`); the frame starts as in the reader constructors, the vtable is `0x00D26CD0`
  (`0x00597AD3`), `+0x08` gets `0xB` and `+0x18` 0, and `+0x1C` is not written.
- `0x0059BD80(frame)` and `0x0059D900(frame)` are Close and IsOpen on the `+0x20` frame alone, for code
  that holds a frame without its stream; `0x001D6E80(frame)` closes one and frees it.
- `0x0059FBA0(frame, offset, origin)` seeks with an origin: through the archive reader (`0x00215220`),
  `SetFilePointer`, or a positive view (`0x0020C180` → `0x00217AD0`), the first that is set, and returns
  −1 when no route is.
- Each `0x0059FBA0` route is a tail jump that returns its own result (`0x0059FBAC`, `0x0059FBC7`,
  `0x0059FBD5`). `SetFilePointer` gets the offset as the low 32 bits with a null high part and the
  origin as the move method; the view route enters `0x0020C180` through `0x001D6CE0`, which adds the cache
  manager (`0x0020C700`).
- `0x0020C180(manager, view, offset, origin)` answers -1 itself for a null view
  (`0x0020C186`-`0x0020C199`) and otherwise jumps to `0x00217AD0(view, offset, origin)`
  (`0x0020C18B`-`0x0020C194`).
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

For step 1, `0x001DB050` builds each of the four prefixes in turn from `0x01DFD010` and the names at
`0x01DFCFE8`, copies that many characters of the name (`strncpy`) and compares them
(`0x001DB161`-`0x001DB195`), returning 1 on the first match and 0 after the fourth. A name no longer than
the prefix never matches (`0x001DB13C`).

### The name filter

Route 1 is skipped for a name of 4 characters or fewer (3 or fewer at `0x0059EF4B`, then 4 at `0x0059EF8A`, after
the first four character tests), and when any one of these
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
- A null name leaves the key empty (`0x0020C443`). The name is first copied whole into a 256-byte stack
  buffer with no length check (`0x0020C480`-`0x0020C48C`), so a name longer than 255 characters overruns it;
  the key goes the same way into the 256-byte buffer `0x0020C1B0` gives (`0x0020C1F6`-`0x0020C213`).
- An empty key returns −1. Otherwise the key is hashed with `0x00674A00` (seed `0x1505`,
  `hash × 33 + (signed char)c`, bit `0x80000000` cleared) and the hash is stored through the key pointer before
  the search.
- Under the manager's lock (`+0x58`), the tree rooted at `+0x38` (header `+0x28`) is searched with
  unsigned compares on each node's dword `+0x20`. A miss returns −1.
- A hit writes the entry's size, then `0x0020C300` builds the view.

`0x0020C300(manager, key, data, size, selector, kind)` adds one to the manager's `+0x88` and to the
entry's byte `+0x10`, then stamps the entry:

- selector 5 and kind 1 to 4: kind `+0x14` becomes 5;
- otherwise kind 5 or selector 5: no stamp;
- otherwise selector 3: word `+0x0E` takes the word at `[manager + 0x18] + 0xE8`;
- otherwise selector 1, 2 or 4: word `+0x0C` takes the manager's word `+0x80`;
- otherwise, selector 0 or above 5: no stamp (`0x0020C398`-`0x0020C3A0`).

It then allocates a 16-byte view `{data, size, position 0}` (`0x00217A60`). When that allocation fails
it returns 0, which the resolver takes as a hit: the stream is left with no readable backing, IsOpen
true, and every Read returning 0.

It finds the entry by key each time it touches it (`0x0020B5F0`) and runs under the manager's lock, which
both of its callers hold: `0x0020C1B0` for a hit (`0x0020C23C`, `0x0020C2A8`) and `0x0020B680` for a key that is
already present (`0x0020B6B3`, `0x0020B726`).

### Reading a cache view

A view read `0x00217A70(view, buffer, n)` returns `FFFFFFFF` for a null buffer. It computes
`position + n` as a 32-bit sum and, when that exceeds the size, takes `size − position` instead; it
copies that many bytes from `data + position` and advances the position. A wrapped sum keeps the full
request. It returns the count it copied; a count of 0 copies nothing and returns 0 (`0x00217AAA`).

A view seek `0x00217AD0(view, offset, origin)` sets the position to the offset (origin 0), the
position plus the offset (1) or the size plus the offset (2), leaves it for any other origin, and then
clamps it to the size; there is no lower clamp. The clamp compares unsigned (`0x00217AFF`), so a position
that would go below 0 lands on the size. The seek returns the new position (`0x00217B05`).

Releasing a view, `0x0020B9A0(manager, key, view)`, takes the lock, finds the entry by key and lowers its
byte `+0x10` by one unless it is 0, and then frees the 16-byte view whether or not the key was found.
It returns 1; a null view returns 0 at once, without the lock (`0x0020B9BA`), and `0x001D6AA0` passes the
answer on as 0 or 1 (`0x001D6AC8`). The cached bytes stay in the cache.

In `0x0020B9A0` the lock is `manager + 0x58`, taken with `0x005CD4F0` and dropped with
`0x005CD820`; the entry is looked up by the dword key `+0x20` in the tree at `manager + 0x28`
(`0x0020B9C0`-`0x0020BA22`). The counted byte is `+0x10` of the object the entry's `+0x28` points
to, not of the entry itself (`0x0020BA0D`-`0x0020BA1B`).
Between the unlock and the free the view goes to `0x0016D6A0`, which only returns
(`0x0020BA2A`); the free is `0x00809950(view, 0x10)` (`0x0020BA2F`-`0x0020BA37`).

`0x0020C150(cache, view, buffer, n)` is the read that slot 5 reaches through `0x001D6CA0`: it calls
`0x00217A70` when the view and the count are both non-zero and returns 0 otherwise.

### Copying an archive hit into the cache

`0x0059A9B0(frame, key)` asks the cache for a buffer of the file's size (`0x001D6BB0` → `0x0020BFA0(cache,
size, selector ≠ 1)`), reads the whole file into it from the archive reader (or the Win32 handle, or a
view), logs `read bytes count is not same as file size (%08x)!` on a short read, closes the archive
reader and the Win32 handle, and inserts the buffer under the key with the selector as its kind
(`0x001D6A20` → `0x0020B680`). The view the insertion returns becomes the stream's `+0x40`, so later reads
come from the cache; a result of 0 or less frees the buffer again.

With no buffer it returns −1 at once and reads and closes nothing (`0x0059A9E1`). The value the log
prints is the key (`0x0059AA47`), and a short read is still inserted, under the full size. The handle
is closed with `SetEndOfFile` and then `CloseHandle` and set to −1 (`0x0059AA7B`-`0x0059AA8B`). The free
after a result of 0 or less goes through `0x001D6B00` (`0x0059AABC`); when the key was already present
`0x0020B680` has freed the buffer before, so a failed view allocation there frees it twice.

`0x0020B680(cache, key, &buffer, size, kind)`, under the lock `+0x58` (`0x0020B6B3`):

- **New key.** It adds a descriptor `{data +0, size +8, word +0x0C, word +0x0E, byte +0x10 = 1,
  kind +0x14}` under the key (`0x0020B5F0`). Kind 5 gets `+0x0C` = 0; kind 3 gets `+0x0E` from
  `[cache + 0x18] + 0xE8`; any other kind gets `+0x0C` from the cache's word `+0x80` and `+0x0E` =
  −1. It returns a new view and adds the size to the cache's byte total `+0x90`.
- The descriptor is a record from the pool (`0x001BA860`, `0x0020B746`). Kind 5 also gets `+0x0E` = 0 (one
  dword store, `0x0020B778`) and kind 3 gets `+0x0C` = 0 (`0x0020B79F`). The lock is released before the
  view is made (`0x0020B7E8`); a failed view allocation returns 0 and leaves the entry with its one view
  counted (`0x0020B802`).
- With the pool empty no descriptor is filed, but the view is still made over the buffer and the size
  still added to `+0x90` (`0x0020B75B`); no entry then holds the buffer, so neither eviction nor the view
  release frees it.
- **Key already present.** It frees the incoming buffer (`0x0020B0F0`) and returns a view of the
  existing entry through `0x0020C300`, which gets this call's kind as its selector and the entry's own
  kind (`0x0020B6F4`-`0x0020B726`).

### The cache's memory budget and eviction

The constructor's first step, `0x0020B0D0`, stores the limit at `+0x00`, `0x10000` in the dword `+0x08`
and 0 as the usage. Cache entries come from a record pool at `+0x98` (`0x0020B150`, built without a
lock of its own; `0x0020B3E0` destroys it); `0x0020C560` sizes its vector, and `0x0020BB10` fills new records
with `{data 0, size 0, +0x0C 0, +0x0E −1, views 0, kind 1}`.

`0x0020B150(pool, n, flag)` zeroes the vector, starts empty sets at pool `+0x20` and `+0x58`, sizes the
vector to n records of `0x18` bytes (`0x0020C560`, which also shrinks a longer one) and files each
record's address in the `+0x20` set (`0x00199DB0`, `0x0020B270`-`0x0020B29F`). The lock at pool `+0x90` is set
up (`0x005CC8A0`) and created only for a non-zero flag (`0x005CD0A0`, `0x0020B2A1`). The cache passes 0
(`0x0020B3B1`) and n = (`[0x01F83448]` >> 31) × 10,000, held to 10,000 to 1,000,000 (`0x0020B37C`-`0x0020B3A6`).
`0x001BA860` hands out records from the `+0x20` set, and 0 when it is empty (`0x001BA887`).


`0x0020B130(cache, size)` refuses an allocation when the usage `+0x10` is above the limit `+0x00`;
otherwise it adds the size to the usage and calls `malloc`. The test runs before the size is added,
so one allocation can take the usage past the limit by its whole size. `0x0020B0F0` subtracts the block's `_msize`
from the usage and frees it.

When the allocation fails, `0x0020BFA0` takes the lock `+0x58` and frees unprotected entries in
ascending key order, walking the key map from its first node (`+0x30`, the header's left link) with `0x0016D6D0`, until
`max(200,000,000, 3 × size)` bytes are released, `3 × size` a 32-bit product (`0x0020BFF0`). It never
reads its third argument.

Each freed entry leaves the byte total, the key map and the count `+0x48`: its buffer goes through
`0x0020B0F0`, its record back to the pool at `+0x98` (`0x002124C0`) and its node to the allocator at `+0x50`
(`0x0020C0C0`). An entry is protected when:

- its byte `+0x10` is non-zero or its kind is 5;
- its word `+0x0E` is not negative and equals `[[cache + 0x18] + 0xE8]`;
- its word `+0x0C` is positive and equals the cache's `+0x80` or `+0x84`.

When the walk reaches the end short of the target it calls `0x0020B840(cache, remaining, 1, 0)`; a walk
that meets the target stops there. It then retries the allocation (`0x0020C10F`). While that fails it
walks again from the first node, unless the last walk reached the end, in which case it returns null
(`0x0020C11C`); it unlocks before it returns (`0x0020C127`).

`0x0020B840` applies the same tests (the `+0x0E` and `+0x0C` ones only while its fourth argument is 0,
the `+0x84` one only while its third is 0), walks twice when the first pass falls short, and returns
whether the walk reached the end of the list. The second walk runs only while the third argument is 0;
it then sets it and asks for what the first walk left (`0x0020B96B`-`0x0020B976`), so the call from
`0x0020BFA0` walks once. An amount of 0 returns 1 at once (`0x0020B86D`).

## Layouts

Stream:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x10` | `...` | name copy | bit `0x1` = borrowed |
| `+0x20` | `...` | frame | the frame; the rows below are its fields |
| `+0x20` | `u32` | size |  |
| `+0x28` | `...` | Win32 handle | -1 |
| `+0x30` | `...` | archive reader | 0 |
| `+0x38` | `u8` | selector |  |
| `+0x40` | `...` | cache view | -1 |
| `+0x48` | `u32` |  | cache key |

Cache entry:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `...` | data |  |
| `+0x08` | `u32` | size |  |
| `+0x0C` | `i16` | word0C |  |
| `+0x0E` | `i16` | word0E |  |
| `+0x10` | `u8` |  | views open |
| `+0x14` | `u32` | kind |  |

Cache view:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `...` | data |  |
| `+0x08` | `u32` | size |  |
| `+0x0C` | `u32` | position |  |

Cache manager:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `...` | limit |  |
| `+0x10` | `...` | usage |  |
| `+0x18` | `...` | owner | `+0xE8` word |
| `+0x20` | `...` | key map | header `+0x28`, root `+0x38` |
| `+0x30` | `...` | first node | the key map's lowest key, where eviction starts |
| `+0x48` | `...` | count |  |
| `+0x58` | `...` | lock |  |
| `+0x80` | `...` | protected word | one of the two protected words |
| `+0x84` | `...` | protected word | one of the two protected words |
| `+0x88` | `...` | hits |  |
| `+0x90` | `...` | bytes |  |
| `+0x98` | `...` | record pool | the entry records (`0x0020B150`) |

| | Route 1 (cache) | Route 2 (archive) |
|---|---|---|
| separator | `\` | `/` |
| case | upper, CRT `toupper` | lower, `A`-`Z` only |
| leading text | skipped to the first letter or digit | `.`, `/`, `\` skipped |
| other | doubled `\` collapsed, trailing spaces stripped | nothing |
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

---

[← Bigfile archive](bigfile-archive.md) | [File requests and the read queue →](file-requests-and-the-read-queue.md)
