---
title: "Phyre modifier codes: the named skinning and morph kernels of PDynamicGeometry, their registry and the weight and matrix-palette fetches"
kind: "system"
category: "PhyreEngine"
addresses: "0x006D58D0, 0x006D5A60, 0x006D5AF0, 0x006D5810, 0x02E9FD60, 0x006C45F0, 0x006C4750, 0x006D6F90, 0x00167FE0, 0x006D9200, 0x006C4470, 0x006D5B60, 0x006D5CC0, 0x006D7380, 0x006D7630, 0x006D78E0, 0x006D7BA0, 0x006D7EA0, 0x006D81A0, 0x006D84A0, 0x006D87D0, 0x006D8B00, 0x01F32110"
---

## What the player sees

A dynamic mesh whose modifier network names these codes is skinned to its skeleton or blended
between morph targets by the CPU. The morph codes are what move a face or a shape key between its
target shapes as their weights change.

## How it works

### The modifier record

A modifier code is a `0x78`-byte `PModifier` record. `0x006D58D0(record, name, fetch, kernel, inputs,
outputs, input table, output table, …)` fills it: the name at `+0x00`, the input and output
descriptions as two arrays the record does not own (count with bit 31 set, as in a `PArray`), the
parameter fetch at `+0x40` and the kernel at `+0x48`, and `0xFFFFFFFF` at `+0x70`.

### The registry

Records are kept on one singly linked list headed by `0x02E9FD60`, linked through `+0x08`.
`0x006D5A60` adds a record at the front; it returns `0x11` for a record without a name and `0x12` when
the name is already registered. `0x006D6F90` unlinks a record.

The dynamic-geometry module's init `0x006C45F0` registers fourteen records after its reflected types,
stopping at the first failure, and its shutdown `0x006C4750` unlinks them again. The nine morph
records are built before `main` by one static initialiser each, `0x00167FE0` (`Morph22`) to
`0x00168760`; the five skinning records are initialised data at `0x01F32110`–`0x01F32310`.

`PModifier` is a named type: its descriptor, built by `0x006D5810`, carries the resolver `0x006D5AF0`,
which looks a name up in the list and returns `0x13` when no code has it, so a reference to a code
is stored as its name and resolved through the list.

### The parameter fetch

A fetch is called with an output buffer and the invocation, and returns the number of bytes its
parameters take; with a null buffer it only returns the size.

- `0x006D9200` (every morph code) writes one float weight per input of the modifier. An input bound to
  a network input (a negative first word in its binding) takes the network instance's weight at
  that input's slot (`+0x14`), or 0 when the slot is past the end of the weight array, which
  `0x006C4470` returns. Any other input, and every input when the instance has no weight array, gets
  1.0.
- `0x006D5CC0` (`Skin`, `SkinVertex`) writes one 64-byte matrix per entry of the input's pair list
  (two `u16` indices per entry): the product (`0x00185100`) of the matrix at the first index in the
  array at `+0x28` and the matrix at the second index in the array of the object at `+0x20`.
- `0x006D5B60` (`SkinLocal`, `SkinLocalTangent`, `SkinVertexLocal`) does the same and multiplies in
  one more matrix, the result of `0x00187460` on the matrix stored just before the `+0x28` array.

### The morph kernels

`MorphNC` blends `N` sources (2, 3 or 4) of `C`-component elements (2, 3 or 4 floats) into one
output. A kernel takes the weights, the element count, the source pointers and the output pointer:

1. it keeps only the sources whose weight is not 0, in order;
2. with none left it zeroes the output;
3. with one left it copies it when its weight is exactly 1.0 and scales it otherwise;
4. with two to four left it writes, per float, the sum of each kept source times its weight.

## Layouts

PModifier record (`0x78`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | name |  |
| `+0x08` | `void*` | next record in the registry |  |
| `+0x10` | `u32` | input count \| 0x80000000 |  |
| `+0x18` | `void*` | input descriptions |  |
| `+0x20` | `u32` | output count \| 0x80000000 |  |
| `+0x28` | `void*` | output descriptions |  |
| `+0x40` | `void*` | parameter fetch |  |
| `+0x48` | `void*` | kernel |  |
| `+0x70` | `u32` | 0xFFFFFFFF |  |

## Shipped data

The fourteen registered codes, read from the records:

| Name | Record | Inputs | Outputs | Fetch | Kernel |
|---|---|---:|---:|---|---|
| `Skin` | `0x01F32110` | 4 | 2 | `0x006D5CC0` | `0x006D5DF0` |
| `SkinLocal` | `0x01F32190` | 4 | 2 | `0x006D5B60` | `0x006D5DF0` |
| `SkinLocalTangent` | `0x01F32210` | 5 | 3 | `0x006D5B60` | `0x006D63D0` |
| `SkinVertex` | `0x01F32290` | 3 | 1 | `0x006D5CC0` | `0x006D6AC0` |
| `SkinVertexLocal` | `0x01F32310` | 3 | 1 | `0x006D5B60` | `0x006D6AC0` |
| `Morph22` | `0x02E9FEF0` | 2 | 1 | `0x006D9200` | `0x006D7380` |
| `Morph23` | `0x02EA0160` | 2 | 1 | `0x006D9200` | `0x006D7630` |
| `Morph24` | `0x02EA03D0` | 2 | 1 | `0x006D9200` | `0x006D78E0` |
| `Morph32` | `0x02E9FFC0` | 3 | 1 | `0x006D9200` | `0x006D7BA0` |
| `Morph33` | `0x02EA0230` | 3 | 1 | `0x006D9200` | `0x006D7EA0` |
| `Morph34` | `0x02EA04A0` | 3 | 1 | `0x006D9200` | `0x006D81A0` |
| `Morph42` | `0x02EA0090` | 4 | 1 | `0x006D9200` | `0x006D84A0` |
| `Morph43` | `0x02EA0300` | 4 | 1 | `0x006D9200` | `0x006D87D0` |
| `Morph44` | `0x02EA0570` | 4 | 1 | `0x006D9200` | `0x006D8B00` |

## Operations

- Find a code by name: `0x006D5AF0(&record, name)`; 0 and the record, or `0x13`.
- Add a code: `0x006D5A60(record)` after `0x006D58D0`; remove it with `0x006D6F90(record)`.

## State

### The morph records' statics

Each morph initialiser owns a `0xD0`-byte static: the `0x78`-byte record, a link at `+0x78`, and five 16-byte
description entries from `+0x80`. It passes `+0x80` to `0x006D58D0` as the input table and `+0xC0` as the output table
(the record's `+0x18` and `+0x28`), then stores the entries itself:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x78` | `void*` | link to the record that was the list head |  |
| `+0x80` | `...` | 4 input description entries, 16 bytes each |  |
| `+0xC0` | `...` | 1 output description entry |  |

```
entry: +0x00 ptr semantic (0 in every morph entry), +0x08 u32 data type
```

All five entries of a code carry the same data type: 1 in `Morph22`, `Morph32` and `Morph42`, 2 in the three
`Morph?3` codes and 3 in the three `Morph?4` codes, so the type is the element's float count minus 1. The input
table always has four entries; a code with two or three inputs fills the entries past its input count too.

The initialisers run in initialiser-table order (`0x008C45C8`-`0x008C4608`): `Morph22`, `Morph32`, `Morph42`,
`Morph23`, `Morph33`, `Morph43`, `Morph24`, `Morph34`, `Morph44`. Each stores the head `0x02E9FDE0` in its `+0x78`
and makes its record the head. No instruction reads the head or a link except these initialisers' own loads of
the head, so nothing walks this list; the registry the resolver uses is `0x02E9FD60`.

[phyre-modifier-codes-state.tsv](phyre-modifier-codes-state.tsv) has one row per static: the head, the eight links
of `Morph23` to `Morph44` and their 80 entry words, with each writer and reader as `function (site, value)`.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02E9FDE0` | `void*` | 0 | head of the morph records' own list, linked through `+0x78`; `Morph44` (`0x02EA0570`) after the last initialiser | the nine initialisers, each its record (`0x0016805B`, `0x0016814B`, `0x0016823B`, `0x0016832B`, `0x0016841B`, `0x0016850B`, `0x001685FB`, `0x001686EB`, `0x001687DB`) | the same nine (`0x00168046`, `0x00168136`, `0x00168226`, `0x00168316`, `0x00168406`, `0x001684F6`, `0x001685E6`, `0x001686D6`, `0x001687C6`) |
| record `+0x78`, 8 rows | `void*` | 0 | the record before it in initialiser order | its initialiser | - |
| entry `+0x00`, 40 rows | `void*` | 0 | semantic: 0 | its initialiser | - |
| entry `+0x08`, 40 rows | `u32` | 0 | data type: 1, 2 or 3 | its initialiser | - |

## Modding notes

- Only these fourteen names resolve; any other name gives `0x13` from the resolver.
- A new code can be added by building a record with `0x006D58D0` and registering it with `0x006D5A60`
  before any asset that uses it loads; names must be unique.
- A morph weight of exactly 0 removes that source from the sum, so a target at weight 0 costs nothing.

## Related

- [Phyre modules](phyre-modules.md): the `PDynamicGeometry` module whose init and shutdown register
  the codes.
- [Phyre field schema](phyre-field-schema.md): how a file's classes, including modifier networks, are
  matched to the executable's.
