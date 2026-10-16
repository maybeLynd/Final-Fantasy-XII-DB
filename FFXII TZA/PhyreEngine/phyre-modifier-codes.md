---
title: "Phyre modifier codes: the named skinning and morph kernels of PDynamicGeometry, their registry and the weight and matrix-palette fetches"
kind: "system"
category: "PhyreEngine"
addresses: "006D58D0, 006D5A60, 006D5AF0, 006D5810, 02E9FD60, 006C45F0, 006C4750, 006D6F90, 00167FE0, 006D9200, 006C4470, 006D5B60, 006D5CC0, 006D7380, 006D7630, 006D78E0, 006D7BA0, 006D7EA0, 006D81A0, 006D84A0, 006D87D0, 006D8B00, 01F32110"
---

## What the player sees

A dynamic mesh whose modifier network names these codes is skinned to its skeleton or blended
between morph targets by the CPU. The morph codes are what move a face or a shape key between its
target shapes as their weights change.

## How it works

### The modifier record

A modifier code is a `78`<sub>h</sub>-byte `PModifier` record. `006D58D0(record, name, fetch, kernel, inputs,
outputs, input table, output table, …)` fills it: the name at `+00`<sub>h</sub>, the input and output
descriptions as two arrays the record does not own (count with bit 31 set, as in a `PArray`), the
parameter fetch at `+40`<sub>h</sub> and the kernel at `+48`<sub>h</sub>, and `FFFFFFFF`<sub>h</sub> at `+70`<sub>h</sub>.

### The registry

Records are kept on one singly linked list headed by `02E9FD60`, linked through `+08`<sub>h</sub>.
`006D5A60` adds a record at the front; it returns `11`<sub>h</sub> for a record without a name and `12`<sub>h</sub> when
the name is already registered. `006D6F90` unlinks a record.

The dynamic-geometry module's init `006C45F0` registers fourteen records after its reflected types,
stopping at the first failure, and its shutdown `006C4750` unlinks them again. The nine morph
records are built before `main` by one static initialiser each, `00167FE0` (`Morph22`) to
`00168760`; the five skinning records are initialised data at `01F32110`–`01F32310`.

`PModifier` is a named type: its descriptor, built by `006D5810`, carries the resolver `006D5AF0`,
which looks a name up in the list and returns `13`<sub>h</sub> when no code has it, so a reference to a code
is stored as its name and resolved through the list.

### The parameter fetch

A fetch is called with an output buffer and the invocation, and returns the number of bytes its
parameters take; with a null buffer it only returns the size.

- `006D9200` (every morph code) writes one float weight per input of the modifier. An input bound to
  a network input (a negative first word in its binding) takes the network instance's weight at
  that input's slot (`+14`<sub>h</sub>), or 0 when the slot is past the end of the weight array, which
  `006C4470` returns. Any other input, and every input when the instance has no weight array, gets
  1.0.
- `006D5CC0` (`Skin`, `SkinVertex`) writes one 64-byte matrix per entry of the input's pair list
  (two `u16` indices per entry): the product (`00185100`) of the matrix at the first index in the
  array at `+28`<sub>h</sub> and the matrix at the second index in the array of the object at `+20`<sub>h</sub>.
- `006D5B60` (`SkinLocal`, `SkinLocalTangent`, `SkinVertexLocal`) does the same and multiplies in
  one more matrix, the result of `00187460` on the matrix stored just before the `+28`<sub>h</sub> array.

### The morph kernels

`MorphNC` blends `N` sources (2, 3 or 4) of `C`-component elements (2, 3 or 4 floats) into one
output. A kernel takes the weights, the element count, the source pointers and the output pointer:

1. it keeps only the sources whose weight is not 0, in order;
2. with none left it zeroes the output;
3. with one left it copies it when its weight is exactly 1.0 and scales it otherwise;
4. with two to four left it writes, per float, the sum of each kept source times its weight.

## Layouts

PModifier record (`78`<sub>h</sub>):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `void*` | name |  |
| `08`<sub>h</sub> | `void*` | next record in the registry |  |
| `10`<sub>h</sub> | `u32` | input count \| `80000000`<sub>h</sub> |  |
| `18`<sub>h</sub> | `void*` | input descriptions |  |
| `20`<sub>h</sub> | `u32` | output count \| `80000000`<sub>h</sub> |  |
| `28`<sub>h</sub> | `void*` | output descriptions |  |
| `40`<sub>h</sub> | `void*` | parameter fetch |  |
| `48`<sub>h</sub> | `void*` | kernel |  |
| `70`<sub>h</sub> | `u32` | `FFFFFFFF`<sub>h</sub> |  |

## Shipped data

The fourteen registered codes, read from the records:

| Name | Record | Inputs | Outputs | Fetch | Kernel |
|---|---|---:|---:|---|---|
| `Skin` | `01F32110` | 4 | 2 | `006D5CC0` | `006D5DF0` |
| `SkinLocal` | `01F32190` | 4 | 2 | `006D5B60` | `006D5DF0` |
| `SkinLocalTangent` | `01F32210` | 5 | 3 | `006D5B60` | `006D63D0` |
| `SkinVertex` | `01F32290` | 3 | 1 | `006D5CC0` | `006D6AC0` |
| `SkinVertexLocal` | `01F32310` | 3 | 1 | `006D5B60` | `006D6AC0` |
| `Morph22` | `02E9FEF0` | 2 | 1 | `006D9200` | `006D7380` |
| `Morph23` | `02EA0160` | 2 | 1 | `006D9200` | `006D7630` |
| `Morph24` | `02EA03D0` | 2 | 1 | `006D9200` | `006D78E0` |
| `Morph32` | `02E9FFC0` | 3 | 1 | `006D9200` | `006D7BA0` |
| `Morph33` | `02EA0230` | 3 | 1 | `006D9200` | `006D7EA0` |
| `Morph34` | `02EA04A0` | 3 | 1 | `006D9200` | `006D81A0` |
| `Morph42` | `02EA0090` | 4 | 1 | `006D9200` | `006D84A0` |
| `Morph43` | `02EA0300` | 4 | 1 | `006D9200` | `006D87D0` |
| `Morph44` | `02EA0570` | 4 | 1 | `006D9200` | `006D8B00` |

## Operations

- Find a code by name: `006D5AF0(&record, name)`; 0 and the record, or `13`<sub>h</sub>.
- Add a code: `006D5A60(record)` after `006D58D0`; remove it with `006D6F90(record)`.

## Modding notes

- Only these fourteen names resolve; any other name gives `13`<sub>h</sub> from the resolver.
- A new code can be added by building a record with `006D58D0` and registering it with `006D5A60`
  before any asset that uses it loads; names must be unique.
- A morph weight of exactly 0 removes that source from the sum, so a target at weight 0 costs nothing.

## Related

- [Phyre modules](phyre-modules.md): the `PDynamicGeometry` module whose init and shutdown register
  the codes.
- [Phyre field schema](phyre-field-schema.md): how a file's classes, including modifier networks, are
  matched to the executable's.
