---
title: "Resource sections: how a section inside a loaded resource is found by tag and name, the @FRP container, resource entries and their two storage modes, and the banked resource tables"
kind: "system"
category: "Game files and data tables"
addresses: "00409C30, 00409210, 02B62E20, 00409780, 00409660, 00409930, 00409A30, 004096C0, 00409600, 0051EE00, 003AB7F0, 0036B130, 02B62E10, 0041E500, 004090D0, 00409F50, 002ED570, 0051FF30, 00409F70, 0040A210, 0051F9F0, 00409F10, 0046E250, 00477EE0, 0041E3A0, 0033263C, 00408F30, 00408FA0"
---

## What the player sees

Nothing directly, but every loaded thing, from a zone's script to a model's mesh or a sound bank, is
reached as a named section inside a larger resource. A hand-edited resource whose section names or
offsets are off is not found, and whatever needed it does not appear.

## How it works

### Matching a section

`00409C30(header, tag, name)` decides whether a section header matches:

- the tag matches when the query tag is 0, when it is `4C4C4140`<sub>h</sub> (the bytes `@ALL`), or when it
  equals the header's dword `+00`<sub>h</sub>;
- the name matches when the query name is NULL, or when all eight dwords of the header's 32-byte name
  at `+10`<sub>h</sub> equal the query's.

A searcher first copies the query name into the shared buffer `02B62E20` with `00409210`: it zeroes
32 bytes, copies at most 32 with `strncpy`, and forces byte `1F`<sub>h</sub> to 0. A query is therefore an
ordinary C string, a stored name must be zero-padded to match, and a name of 32 characters can never
match, because its last byte is cleared in the query but not in the header. The buffer is a single
global, so a by-name search is not re-entrant.

### Searching a resource

`00409780(entry, tag, name, &index, &offset)` sets both outputs to −1, resolves the entry's base (below)
and returns when it is null. Then:

- **`@FRP` container** (first dword `50524640`<sub>h</sub>). With version 0 (`+04`<sub>h</sub> = 0) a matching container
  header gives offset 0 and index 0; otherwise it walks the `count` (`+0C`<sub>h</sub>) dwords of the offset
  table at `+30`<sub>h</sub> and the first section `30h + table[i]` that matches gives offset `table[i] + 30h`
  and index i. Version 1 does the same with the table at `+40`<sub>h</sub> and offsets `+ 40h`, skipping zero
  entries. Any other version finds nothing.
- **Any other header.** A match gives offset 0 and index 0.

Its callers are `00409660` (find and resolve to a pointer), `00409930` (the index alone), `00409A30`
(the offset alone) and `00409960`. A found offset is 0 or a stored table entry plus `30`<sub>h</sub> or
`40`<sub>h</sub>, so a −1 that is not "not found" needs a stored entry of `−31h` or `−41h`, a section placed
before its container.

`00408F90` (from index 0) and `00408FA0(container, tag, name, start)` search an `@FRP` container
directly: a section matches on its exact tag (no wildcards) and, when a name is given, on `00408F30`, an
eight-dword compare that takes the container's own name at `+10`<sub>h</sub>, not the section's. They return the
index, or −1.

### Resolving an offset

`004096C0(entry, offset)` returns NULL for a null entry or an offset of −1. Otherwise it adds the
offset to the low 32 bits of the entry's base and sign-extends the 32-bit sum, and `00409660` does the
same. A base above 4 GB does not survive, and nothing tests the base: an entry whose base resolves to
0 still returns the offset itself as a pointer.

### Resource entries and their base

`00409600(entry)`:

- mode `+04`<sub>h</sub> = 0: `0051EE00(entry + 10h)`, which decodes the handle at `entry + 18h`;
- mode 1: while the byte `02B62E10` is set, it decodes the handle at `+30`<sub>h</sub> and stores the result at
  `+38`<sub>h</sub>; otherwise it returns `+38`<sub>h</sub> as cached;
- any other mode: 0.

`003AB7F0(h)` decodes a handle: 0 gives 0; a value with its low two bits clear is a plain pointer;
otherwise `0036B130` looks up the low 32 bits (for `h ≥ 100000h` with low bits set it returns
`[(h & ~3) + 8] + 40h`), and a result whose low 32 bits are `40`<sub>h</sub> or less gives 0.

`0041E500(root)`, the only writer of `02B62E10`, sets it, refreshes every row of the descriptor at
`root + D90h` (`00409F70`), clears it, and then refreshes the other three containers at `+D98`<sub>h</sub>,
`+DA8`<sub>h</sub> and `+DA0`<sub>h</sub>.

### The @FRP child selector

`004090D0(container, row, col)` returns NULL for NULL and the input unchanged for anything that is not
`@FRP`. Version 0: the child `low32(container) + 30h + table[col]`, or the first child when `col` is
at or past the count. Version 1: the index is `row × [+30h] + col` when `row` is below `[+34h]`,
otherwise `col`; a zero table entry gives NULL, an index at or past the count gives NULL, else
`low32(container) + 40h + table[index]`. Both return the sum zero-extended, unlike the sign-extending
section helpers.

### Banked resource tables

A resource entry is a row in a bank owned by a table descriptor. `002ED570(descriptor, index)`:

1. refreshes the slot table `+38`<sub>h</sub> from its handle `+30`<sub>h</sub>, and the bank directory `+10`<sub>h</sub> from its
   handle `+08`<sub>h</sub>, when those handles are set;
2. reads the bank address from the directory record `index >> bankShift` (`+10`<sub>h</sub> of a 32-byte record,
   decoded with `0020E600`), before any test;
3. returns NULL when the slot `index` (16 bytes) has key −1;
4. otherwise returns `bank + sign32((index & rowMask) × rowStride)`.

Nothing bounds the index against the capacity `+54`<sub>h</sub> or against 0.

`00409F50(descriptor, id)` returns NULL for an id word of `FFFF`<sub>h</sub> and otherwise passes the word,
sign-extended, to `002ED570`, so ids `8000`<sub>h</sub> to `FFFE`<sub>h</sub> become negative indices that read before the
slot table and the directory. `0051FF30(descriptor, fn)` walks the slot list from `+40`<sub>h</sub> through each
slot's `+08`<sub>h</sub> until −1 and calls `fn` on each row; `00409F70` uses it with `0040A210`, which re-decodes
each row's handle `+30`<sub>h</sub> into `+38`<sub>h</sub>.

`0051F9F0(descriptor, rowStride, bankShift, bankCount, directory, slots)` is the only writer of the
geometry: it stores the stride and shift, derives `rowMask` = `(1 << shift) − 1` and the capacity
`(1 << shift) × bankCount`, clears the directory and slot buffers, allocates one blob of
`(bankCount << shift) × rowStride` bytes in arena 6 into `+28`<sub>h</sub>, points each directory record at its
bank, and sets flag bit 0. Its three callers are inside the render root builder `0041E3A0` (called from
`0033263C`):

| Builder | Descriptor | Row stride | Shift | Banks | Capacity | Directory | Slots |
|---|---|---|---|---|---|---|---|
| `00409F10` | root `+D90`<sub>h</sub> | `50`<sub>h</sub> | 5 | 10 | 320 | `02B62E40` | `02B62F80` |
| `0046E250` | root `+D98`<sub>h</sub> | `C0`<sub>h</sub> | 5 | 5 | 160 | `02CA61B0` | `02CA6250` |
| `00477EE0` | root `+DA0`<sub>h</sub> | `260`<sub>h</sub> | 5 | 5 | 160 | `02CA74A0` | `02CA7540` |

## Layouts

```python
section header  0x30: +0x00 u32 tag, +0x10 char[32] name (zero-padded)
@FRP container  +0x00 '@FRP' (0x50524640), +0x04 u32 version (0 or 1), +0x0C u32 count,
                v0: +0x30 u32[count] offsets from +0x30; v1: +0x30 u32 columns, +0x34 u32 rows, +0x40 u32[count] offsets from +0x40 (0 = empty)
resource entry  +0x04 u32 mode, +0x18 inline handle (mode 0), +0x30 handle, +0x38 cached base (mode 1)
descriptor      +0x08 directory handle, +0x10 directory (0x20-byte records, +0x10 encoded bank address),
                +0x28 bank blob, +0x30 slot handle, +0x38 slots (0x10 each: +0x00 s32 key, -1 empty; +0x08 s32 next),
                +0x40 s32 first slot, +0x48 s32 row stride, +0x4C u32 bank shift, +0x50 u32 row mask, +0x54 u32 capacity
```

The shared name buffer is listed in
[`resource-sections-name-scratch-accesses.tsv`](resource-sections-name-scratch-accesses.tsv).

## Operations

Per search: one name copy and at most `count` header compares. Per row lookup: two handle decodes and
one multiply.

## State

The name buffer `02B62E20`, the re-resolve byte `02B62E10`, and each descriptor's directory, slots and
bank blob.

## Modding notes

- Section names are at most 31 characters and must be zero-padded in the header.
- `@ALL` is a query wildcard and `@FRP` marks a container; every other tag, `@FEF` included, matches
  only exactly.
- An entry whose base does not resolve still yields `0 + offset`; test the base, not only the result.
- A relocated mode-1 resource keeps a stale cached base until `0041E500` runs.

## Related

- [The resource owner](resource-ownership-and-disposal.md): how a loaded resource is owned and released.
- [FRP object container](../17-Presentation-Rendering/model-files-cm-ca.md
): the `@FRP` files on disk.
