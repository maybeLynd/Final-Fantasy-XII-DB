[Home](../../README.md) / [Game files and data tables](README.md) / Resource sections

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Resource sections: how a section inside a loaded resource is found by tag and name, the @FRP container, resource entries and their two storage modes, and the banked resource tables | system | Game files and data tables | Loaded resources | How the engine reaches a piece of data inside a loaded resource: the tag and 32-byte name match with its @ALL and NULL wildcards and the 31-character name limit, the @FRP container header with its version 0 and version 1 offset tables, the section search and its -1 sentinel, the child selector, resource entries with an inline or handle-and-cache base and the re-resolve flag, the handle decoding, and the banked resource tables that hold entries as rows: their descriptor, row lookup, refresh walk and the three tables the render root builds. | 0x00409C30, 0x00409210, 0x02B62E20, 0x00409780, 0x00409660, 0x00409930, 0x00409A30, 0x004096C0, 0x00409600, 0x0051EE00, 0x003AB7F0, 0x0036B130, 0x02B62E10, 0x0041E500, 0x004090D0, 0x00409F50, 0x002ED570, 0x0051FF30, 0x00409F70, 0x0040A210, 0x0051F9F0, 0x00409F10, 0x0046E250, 0x00477EE0, 0x0041E3A0, 0x0033263C, 0x00408F30, 0x00408FA0 |

## What the player sees

Nothing directly, but every loaded thing, from a zone's script to a model's mesh or a sound bank, is
reached as a named section inside a larger resource. A hand-edited resource whose section names or
offsets are off is not found, and whatever needed it does not appear.

An `@FRP` container is a list of sections, each with a four-letter tag and a name of up to 31 characters. The game
finds a piece by walking the container's offset list for the first section whose tag and name match the ones asked
for.

## How it works

### Matching a section

`0x00409C30(header, tag, name)` decides whether a section header matches:

- the tag matches when the query tag is 0, when it is `0x4C4C4140` (the bytes `@ALL`), or when it
  equals the header's dword `+0x00`;
- the name matches when the query name is NULL, or when all eight dwords of the header's 32-byte name
  at `+0x10` equal the query's.

A searcher first copies the query name into the shared buffer `0x02B62E20` with `0x00409210`: it zeroes
32 bytes, copies at most 32 with `strncpy`, and forces byte `0x1F` to 0. A query is therefore an
ordinary C string, a stored name must be zero-padded to match, and a name of 32 characters can never
match, because its last byte is cleared in the query but not in the header. The buffer is a single
global, so a by-name search is not re-entrant.

### Searching a resource

`0x00409780(entry, tag, name, &index, &offset)` sets both outputs to −1¹, copies
a given name into `0x02B62E20`², resolves the entry's base (below) and returns when the entry
is null, its mode is neither 0 nor 1, or the base is null³. Then:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x004097AA`, `0x004097B0` |
| ² | `0x004097C9` |
| ³ | `0x004097D1`, `0x004097E1`, `0x00409814` |

</details>

- **`@FRP` container** (first dword `0x50524640`). With version 0 (`+0x04` = 0) a matching container
  header gives offset 0 and leaves the index at −1 (`0x004098B1`-`0x004098B4` skip the index store at
  `0x0040990F`); otherwise it walks the `count` (`+0x0C`) dwords of the offset table at `+0x30` and the
  first section `0x30 + table[i]` that matches gives offset `table[i] + 0x30` and index i.
- **`@FRP` container, version 1.** It does the same with the table at `+0x40` and offsets `+ 0x40`,
  skipping zero entries; its matching container header also gives offset 0 and index −1
 ¹. Any other version finds nothing.
- **Any other header.** A match gives offset 0 and index 0².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00409840`-`0x00409848` |
| ² | `0x00409909`-`0x0040990F` |

</details>

Its callers are `0x00409660` (find and resolve to a pointer), `0x00409930` (the index alone), `0x00409A30`
(the offset alone) and `0x00409960`; `0x00409930` therefore returns −1 when the container header itself
is the match. A found offset is 0 or a stored table entry plus `0x30` or `0x40`, so a −1 that is not
"not found" needs a stored entry of `−0x31` or `−0x41`, a section placed before its container.

`0x00408F90` (from index 0) and `0x00408FA0(container, tag, name, start)` search an `@FRP` container
directly: a section matches on its exact tag (no wildcards) and, when a name is given, on `0x00408F30`, an
eight-dword compare that takes the container's own name at `+0x10`, not the section's. They return the
index, or −1. The name is compared as given, without the shared buffer.

`0x00408F30` returns 0 when all eight dwords are equal and 1 otherwise, and `0x00408FA0` takes the section
when the result is not 0¹. With a name, a section of the tag is therefore
taken while the container's name differs from the query, and a container whose name equals the query
gives −1. The four callers of `0x00408F90`² give the tag
`@FRM` and no name.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0040900E`, `0x0040906E` |
| ² | `0x00422DB6`, `0x0042340D`, `0x004234DC`, `0x00423531` |

</details>

`0x00408FA0` walks from `start` to `count` (`+0x0C`) and gives −1 for a null or non-`@FRP` input, a
version above 1, or a `start` at or past `count`¹. Version 1 does
not skip zero table entries², and each section address is a 32-bit sum.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00408FC7`-`0x00408FE4`, `0x0040903B` |
| ² | `0x00408FF0`-`0x00408FF5` |

</details>

### Resolving an offset

`0x004096C0(entry, offset)` returns NULL for a null entry or an offset of −1. Otherwise it adds the
offset to the low 32 bits of the entry's base and sign-extends the 32-bit sum¹, and
`0x00409660` does the same². The pointer is right only while base + offset lies below
2 GB³: from 2 GB to 4 GB it comes back with the top 32 bits set, and a base above 4 GB loses
its top 32 bits. Nothing tests the base: an entry whose base resolves to 0 still returns the offset itself
as a pointer.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x004096DF`-`0x004096E1` |
| ² | `0x004096A4`-`0x004096A8` |
| ³ | `0x80000000` |

</details>

`0x00409660(entry, tag, name)` returns NULL for a null entry¹ and when `0x00409780` gives the
offset −1², which it does for a base that resolves to 0, so its sum is formed only after a
non-null base; it resolves the base a second time for the sum³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0040966F` |
| ² | `0x0040969A` |
| ³ | `0x0040969F` |

</details>

### Resource entries and their base

`0x00409600(entry)` returns 0 for a null entry¹; otherwise:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00409609` |

</details>

- mode `+0x04` = 0: `0x0051EE00(entry + 0x10)`, which decodes the handle at `entry + 0x18`;
- mode 1: while the byte `0x02B62E10` is set, it decodes the handle at `+0x30` and stores the result at
  `+0x38`; otherwise it returns `+0x38` as cached;
- any other mode: 0.

`0x003AB7F0(h)` decodes a handle: 0 gives 0; a value with its low two bits clear is a plain pointer;
otherwise `0x0036B130` looks up the low 32 bits (for `h ≥ 0x100000` with low bits set it returns
`[(h & ~3) + 8] + 0x40`), and a result whose low 32 bits are `0x40` or less gives 0.

`0x0041E500(root)`, the only writer of `0x02B62E10`, sets it, refreshes every row of the descriptor at
`root + 0xD90`¹, clears it, and then refreshes the other three containers at `+0xD98`,
`+0xDA8` and `+0xDA0`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00409F70` |

</details>

### The @FRP child selector

`0x004090D0(container, row, col)` returns NULL for NULL and the input unchanged for anything that is not
`@FRP`. Version 0: the child `low32(container) + 0x30 + table[col]`, or the first child when `col` is
at or past the count. Version 1: the index is `row × [+0x30] + col` when `row` is below `[+0x34]`,
otherwise `col`; a zero table entry gives NULL, an index at or past the count gives NULL, else
`low32(container) + 0x40 + table[index]`. Both return the sum zero-extended, unlike the
sign-extending section helpers.

Version 1 reads the table entry before it tests the index against the count¹.
Any other version gives NULL².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00409107`, `0x00409113` |
| ² | `0x004090F0` |

</details>

The only tag the selector compares is the container's `@FRP`¹; the child it returns may carry any tag.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x004090DA` |

</details>

### Banked resource tables

A resource entry is a row in a bank owned by a table descriptor. `0x002ED570(descriptor, index)`:

1. refreshes the slot table `+0x38` from its handle `+0x30`, and the bank directory `+0x10` from its
   handle `+0x08`, when those handles are set;
2. reads the bank address from the directory record `index >> bankShift` (`+0x10` of a 32-byte record,
   decoded with `0x0020E600`), before any test;
3. returns NULL when the slot `index` (16 bytes) has key −1;
4. otherwise returns `bank + sign32((index & rowMask) × rowStride)`.

Nothing bounds the index against the capacity `+0x54` or against 0.

`0x00409F50(descriptor, id)` returns NULL for an id word of `0xFFFF` and otherwise passes the word,
sign-extended, to `0x002ED570`, so ids `0x8000` to `0xFFFE` become negative indices that read before the
slot table and the directory.

`0x0051FF30(descriptor, fn)` walks the slot list from `+0x40` through each slot's `+0x08` until −1 and
calls `fn` on each row; with `+0x40` at −1 it calls nothing¹. It finds each row as
`0x002ED570` does and passes NULL for a slot whose key is −1²; it reads the next index after
`fn` returns, from the slot address taken before the call³. `0x00409F70` uses it with
`0x0040A210`, which re-decodes each row's handle `+0x30` into `+0x38`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0051FF45` |
| ² | `0x0051FFCE` |
| ³ | `0x0051FFE4` |

</details>

`0x0051F9F0(descriptor, rowStride, bankShift, bankCount, directory, slots)` is the only writer of the
geometry: it stores the stride and shift, derives `rowMask` = `(1 << shift) − 1` and the capacity
`(1 << shift) × bankCount`, clears the directory and slot buffers, allocates one blob of
`(bankCount << shift) × rowStride` bytes in arena 6 into `+0x28`, points each directory record at its
bank, and sets flag bit `0x1`.

In detail¹: it zeroes the flags, the handles `+0x08` and `+0x30`, the used
count `+0x58`, the high-water word `+0x26` and the current page and page count `+0x20`/`+0x22`, sets
the page list `+0x18`/`+0x1C` and the slot list `+0x40`/`+0x44` to −1 and stores the bank count in the
word `+0x24`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0051FA17`-`0x0051FB4E` |

</details>

Each directory record gets −1 in `+0x00`, `+0x04` and `+0x08` and 0 in the qword `+0x14`; each slot
gets −1 in `+0x00`, `+0x04` and `+0x08` and the encoded null in `+0x0C`. Each bank address is encoded
from its low 32 bits¹, and bank 0 is claimed² before the flag is set.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0020E620` |
| ² | `0x0051F6B0` |

</details>

Its three callers are inside the render root builder `0x0041E3A0` (called from
`0x0033263C`):

| Builder | Descriptor | Row stride | Shift | Banks | Capacity | Directory | Slots |
|---|---|---|---|---|---|---|---|
| `0x00409F10` | root `+0xD90` | `0x50` | 5 | 10 | 320 | `0x02B62E40` | `0x02B62F80` |
| `0x0046E250` | root `+0xD98` | `0xC0` | 5 | 5 | 160 | `0x02CA61B0` | `0x02CA6250` |
| `0x00477EE0` | root `+0xDA0` | `0x260` | 5 | 5 | 160 | `0x02CA74A0` | `0x02CA7540` |

Each descriptor is the object a root qword points to: the builders get `[root + 0xD90]`, `[root + 0xD98]` and
`[root + 0xDA0]`¹. `0x0046E250` then sets the dword at descriptor `+0x60` to 1
and sizes a strided array there with `0x00537270(descriptor + 0x60, 2, bankCount × 32, NULL)`: 160 two-byte elements
and no callback (`0x0046E28A`-`0x0046E2AB`;
[resource ownership](resource-ownership-and-disposal.md#borrowed-views)).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0041E439`, `0x0041E447`, `0x0041E459` |

</details>

## Layouts

<details>
<summary>Show the memory layouts</summary>

Section header (`0x30`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | tag |  |
| `+0x08` | `u32` | length | header included; the @FRM consumer requires more than `0x30` (`0x0041D33F`) |
| `+0x0C` | `u32` | count | records in the section: the @FTR consumer multiplies it by `0x149` (`0x003712FE`), the @FLD consumer bounds its loop by it (`0x0041FFAF`) |
| `+0x10` | `char[32]` | name | zero-padded |

@FRP container:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `...` | magic | '@FRP' (`0x50524640`) |
| `+0x04` | `u32` | version | 0 or 1 |
| `+0x0C` | `u32` | count |  |
| `+0x30` | `...` | offsets | v0: u32[count] offsets from `+0x30` |
| `+0x30` | `u32` | columns | v1 |
| `+0x34` | `u32` | rows | v1 |
| `+0x40` | `...` | offsets | v1: u32[count] offsets from `+0x40` (0 = empty) |

Resource entry:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x04` | `u32` | mode |  |
| `+0x18` | `...` | inline handle | mode 0 |
| `+0x30` | `...` | handle |  |
| `+0x38` | `...` | cached base | mode 1 |

Descriptor:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x08` | `...` |  | directory handle |
| `+0x10` | `...` | directory | `0x20`-byte records, `+0x10` encoded bank address |
| `+0x28` | `...` |  | bank blob |
| `+0x30` | `...` |  | slot handle |
| `+0x38` | `...` | slots | `0x10` each: `+0x00` s32 key, -1 empty; `+0x08` s32 next |
| `+0x40` | `i32` |  | first slot |
| `+0x48` | `i32` |  | row stride |
| `+0x4C` | `u32` |  | bank shift |
| `+0x50` | `u32` |  | row mask |
| `+0x54` | `u32` | capacity |  |

The 13 instructions that read or write the shared name buffer, in `0x00409210` and `0x00409C30`, are listed in
[`resource-sections-name-scratch-accesses.tsv`](resource-sections-name-scratch-accesses.tsv). The name itself is
copied in by the C library's `strncpy`, which `0x00409210` calls¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0040922E` |

</details>

</details>

## Operations

Per search: one name copy and at most `count` + 1 header compares (the container's own header, then each
section). Per row lookup: two handle decodes and one multiply.

## State

<details>
<summary>Show the state it keeps</summary>

The name buffer `0x02B62E20`, the re-resolve byte `0x02B62E10`, and each descriptor's directory, slots and
bank blob.

</details>

## Modding notes

- Section names are at most 31 characters and must be zero-padded in the header.
- `@ALL` is a query wildcard and `@FRP` marks a container; every other tag, `@FEF` included, matches
  only exactly.
- An entry whose base does not resolve still yields `0 + offset`; test the base, not only the result.
- A relocated mode-1 resource keeps a stale cached base until `0x0041E500` runs.

## Related

- [The resource owner](resource-ownership-and-disposal.md): how a loaded resource is owned and released.
- [FRP object container](../Graphics/model-files-cm-ca.md): the `@FRP` files on disk.
