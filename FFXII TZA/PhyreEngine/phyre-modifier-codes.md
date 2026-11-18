[Home](../../README.md) / [PhyreEngine](README.md) / Phyre modifier codes

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Phyre modifier codes: the named skinning and morph kernels of PDynamicGeometry, their registry and the weight and matrix-palette fetches | system | PhyreEngine | Drawing and shaders | The fourteen PModifier codes that PhyreEngine's dynamic-geometry module registers by name: five skinning codes and nine morph-blend codes (Morph22 to Morph44), the 0x78-byte record that pairs a parameter fetch with a kernel, the name registry a file's modifier network resolves against, how the morph weight fetch reads a network instance's weights, how the skinning fetches build the matrix palette, and how the morph kernels blend up to four weighted sources. | 0x006D58D0, 0x006D5A60, 0x006D5AF0, 0x006D5810, 0x02E9FD60, 0x006C45F0, 0x006C4750, 0x006D6F90, 0x00167FE0, 0x006D9200, 0x006C4470, 0x006D5B60, 0x006D5CC0, 0x006D7380, 0x006D7630, 0x006D78E0, 0x006D7BA0, 0x006D7EA0, 0x006D81A0, 0x006D84A0, 0x006D87D0, 0x006D8B00, 0x01F32110 |

## What the player sees

A dynamic mesh whose modifier network names these codes is skinned to its skeleton or blended
between morph targets by the CPU. The morph codes are what move a face or a shape key between its
target shapes as their weights change.

A model file stores each modifier code as its name, and the game looks the name up in its list of fourteen codes. Each
code pairs a step that gathers its inputs, the morph weights or the bone matrices, with a step that does the blending
or skinning.

## How it works

### The modifier record

A modifier code is a `0x78`-byte `PModifier` record. `0x006D58D0(record, name, fetch, kernel, inputs,
outputs, input table, output table, …)` fills it: the name at `+0x00`, the input and output
descriptions as two arrays the record does not own (count with bit `0x80000000` set, as in a `PArray`), the
parameter fetch at `+0x40` and the kernel at `+0x48`, and `0xFFFFFFFF` at `+0x70`.

It also zeroes the link `+0x08` and the qwords `+0x30`, `+0x38`, `+0x60` and `+0x68`¹, stores its ninth argument at `+0x58` and the dword of its eleventh
at `+0x50`², and returns the record³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x006D58DA`, `0x006D5914`, `0x006D5920`-`0x006D5928` |
| ² | `0x006D5906`, `0x006D590E` |
| ³ | `0x006D5911` |

</details>

### The registry

Records are kept on one singly linked list headed by `0x02E9FD60`, linked through `+0x08`.
`0x006D5A60` adds a record at the front; it returns `0x11` for a record without a name and `0x12` when
the name is already registered. `0x006D6F90` unlinks a record.

`0x006D6F90` also clears the record's link `+0x08`¹. A record that is not on the
list is left as it is, and the body returns 0 on every path².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x006D6FD7`, `0x006D6FDA` |
| ² | `0x006D6FCD`, `0x006D6FDE` |

</details>

The dynamic-geometry module's init `0x006C45F0` registers fourteen records after its reflected types,
stopping at the first failure, and its shutdown `0x006C4750` unlinks them again. The nine morph
records are built before `main` by one static initialiser each, `0x00167FE0` (`Morph22`) to
`0x00168760`; the five skinning records are initialised data at `0x01F32110`–`0x01F32310`.

Both go through the records in one order: `Morph22`, `Morph32`, `Morph42`, `Morph23`, `Morph33`,
`Morph43`, `Morph24`, `Morph34`, `Morph44`, then `Skin`, `SkinLocal`, `SkinLocalTangent`, `SkinVertex`
and `SkinVertexLocal`. The init registers through the jump `0x006D5A50` to `0x006D5A60`.

On a failure the init returns that code, `0x11` or `0x12`¹, which stops the module init
walk; otherwise it returns the last registration's result (tail jump at `0x006C473F`). The shutdown
stops at the first non-zero result of `0x006D6F90`²; that body always returns 0, so the
shutdown unlinks all fourteen and returns 0 (tail jump at `0x006C4847`).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x006C4744` |
| ² | `0x006C4762` |

</details>

`PModifier` is a named type: its descriptor, built by `0x006D5810`, carries the resolver `0x006D5AF0`,
which looks a name up in the list and returns `0x13` when no code has it, so a reference to a code
is stored as its name and resolved through the list. A null name also gives `0x13`, and with `0x13`
the record pointer is set to null¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x006D5AFD`, `0x006D5B46` |

</details>

`0x006D5810` builds the descriptor once, behind the guard `0x02E9FDD0`, at `0x02E9FD70`. It gives `0x006B6820`
the type name at `0x00D8D7A0`, `0x78`, 8, `0x006CD4C0` (which gives a record's name and the name's length
plus 1) and the resolver¹. It then sets the descriptor's vtable `0x00D8D7B8`²,
registers `0x008B7590` with `atexit`³ and returns `0x02E9FD70` on every call.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x006D588A` |
| ² | `0x006D5896` |
| ³ | `0x006D58A4` |

</details>

`0x008B7590` is two instructions: it loads the descriptor's address `0x02E9FD70` as the one argument and
jumps to `0x006B68A0`¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x008B7590`-`0x008B7597` |

</details>

### The parameter fetch

A fetch is called with an output buffer and the invocation, and returns the number of bytes its
parameters take; with a null buffer it only returns the size.

- `0x006D9200` (every morph code) writes one float weight per input of the modifier. An input bound to
  a network input (a negative first word in its binding) takes the network instance's weight at
  that input's slot (`+0x14`), or 0 when the slot is past the end of the weight array, which
  `0x006C4470` returns. Any other input, and every input when the instance has no weight array, gets
  1.0.
- `0x006D5CC0` (`Skin`, `SkinVertex`) writes one 64-byte matrix per entry of the input's pair list
  (two `u16` indices per entry): the product¹ of the matrix at the first index in the
  array at `+0x28` and the matrix at the second index in the array of the object at `+0x20`.
- `0x006D5B60` (`SkinLocal`, `SkinLocalTangent`, `SkinVertexLocal`) does the same and multiplies in
  one more matrix, the result of `0x00187460` on the matrix stored just before the `+0x28` array. That
  matrix comes first: `0x00185100` takes it and the first-index matrix², then takes that
  product and the second-index matrix³.
- In both skinning fetches the offsets are on the invocation's first pointer: the pair list is at
  `+0x38` (count `+0x08`, bit `0x80000000` masked; entries `+0x10`), and the object is the pointer
  stored first at `+0x20`, with its array at `+0x18`⁴.
  The size returned is the count × 64 on every path⁵.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00185100` |
| ² | `0x006D5BF1` |
| ³ | `0x006D5C04` |
| ⁴ | `0x006D5CC9`-`0x006D5CFF`, `0x006D5B6D`-`0x006D5BAC` |
| ⁵ | `0x006D5CDC`, `0x006D5B80` |

</details>

### The morph kernels

`MorphNC` blends `N` sources (2, 3 or 4) of `C`-component elements (2, 3 or 4 floats) into one
output. A kernel takes the weights, the element count, the source pointers and the output pointer:

1. it keeps only the sources whose weight is not 0, in order;
2. with no source left it zeroes the output;
3. with one left it copies it when its weight is exactly 1.0 and scales it otherwise;
4. with two to four left it writes, per float, the sum of each kept source times its weight.

## Layouts

<details>
<summary>Show the memory layouts</summary>

PModifier record (`0x78`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | name |  |
| `+0x08` | `void*` |  | next record in the registry |
| `+0x10` | `u32` |  | input count \| `0x80000000` |
| `+0x18` | `void*` |  | input descriptions |
| `+0x20` | `u32` |  | output count \| `0x80000000` |
| `+0x28` | `void*` |  | output descriptions |
| `+0x30` | `u64` |  | 0 from `0x006D58D0` |
| `+0x38` | `u64` |  | 0 from `0x006D58D0` |
| `+0x40` | `void*` |  | parameter fetch |
| `+0x48` | `void*` | kernel |  |
| `+0x50` | `u32` |  | `0x006D58D0`'s eleventh argument |
| `+0x58` | `u64` |  | `0x006D58D0`'s ninth argument |
| `+0x60` | `u64` |  | 0 from `0x006D58D0` |
| `+0x68` | `u64` |  | 0 from `0x006D58D0` |
| `+0x70` | `u32` |  | value `0xFFFFFFFF` |

</details>

## Shipped data

<details>
<summary>Show the shipped data</summary>

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

</details>

## Operations

- Find a code by name: `0x006D5AF0(&record, name)`; 0 and the record, or `0x13` and a null record.
- Add a code: `0x006D5A60(record)` after `0x006D58D0`; remove it with `0x006D6F90(record)`.

## State

<details>
<summary>Show the state it keeps</summary>

### The morph records' statics

Each morph initialiser owns a `0xD0`-byte static: the `0x78`-byte record, a link at `+0x78`, and five 16-byte
description entries from `+0x80`. It passes `+0x80` to `0x006D58D0` as the input table and `+0xC0` as the output table
(the record's `+0x18` and `+0x28`), then stores the entries itself:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x78` | `void*` |  | link to the record that was the list head |
| `+0x80` | `...` |  | 4 input description entries, 16 bytes each |
| `+0xC0` | `...` |  | 1 output description entry |

```
entry: +0x00 ptr semantic (0 in every morph entry), +0x08 u32 data type
```

All five entries of a code carry the same data type: 1 in `Morph22`, `Morph32` and `Morph42`, 2 in the three
`Morph?3` codes and 3 in the three `Morph?4` codes, so the type is the element's float count minus 1. The input
table always has four entries; a code with two or three inputs fills the entries past its input count too.

Two more steps belong to each initialiser:

- It gives `0x006D58D0` 0 as the ninth and eleventh arguments, so the record's `+0x58` and `+0x50` are 0
  (`Morph22`: `0x0016800A`, `0x00167FF3`).
- It ends with a tail jump to `atexit`¹ for its exit teardown, which passes the record to
  `0x006D5940`: the nine teardowns `0x008B7610` to `0x008B7690`, `0x10` apart, in the initialisers' address order
  (`Morph22`, `Morph23`, `Morph24`, `Morph32`, `Morph33`, `Morph34`, `Morph42`, `Morph43`, `Morph44`).
  - That is not the order they run in (`Morph22`: `0x008B7610`, jump at `0x001680C1`; `Morph23`: `0x008B7620`, loaded
    at `0x0016813D`; `Morph44`: `0x008B7690`, jump at `0x00168841`).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00808B90` |

</details>

The initialisers run in initialiser-table order¹: `Morph22`, `Morph32`, `Morph42`,
`Morph23`, `Morph33`, `Morph43`, `Morph24`, `Morph34`, `Morph44`. Each stores the head `0x02E9FDE0` in its `+0x78`
and makes its record the head. No instruction reads the head or a link except these initialisers' own loads of
the head, so nothing walks this list; the registry the resolver uses is `0x02E9FD60`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x008C45C8`-`0x008C4608` |

</details>

[phyre-modifier-codes-state.tsv](phyre-modifier-codes-state.tsv) has one row per static: the head, the nine links
of `Morph22` to `Morph44` and their 90 entry words, with each writer and reader as `function (site, value)`.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02E9FDE0` | `void*` | 0 | head of the morph records' own list, linked through `+0x78`; `Morph44` (`0x02EA0570`) after the last initialiser | the nine initialisers, each its record (`0x0016805B`, `0x0016814B`, `0x0016823B`, `0x0016832B`, `0x0016841B`, `0x0016850B`, `0x001685FB`, `0x001686EB`, `0x001687DB`) | the same nine (`0x00168046`, `0x00168136`, `0x00168226`, `0x00168316`, `0x00168406`, `0x001684F6`, `0x001685E6`, `0x001686D6`, `0x001687C6`) |
| record `+0x78`, 8 rows | `void*` | 0 | the record before it in initialiser order | its initialiser | - |
| entry `+0x00`, 40 rows | `void*` | 0 | semantic: 0 | its initialiser | - |
| entry `+0x08`, 40 rows | `u32` | 0 | data type: 1, 2 or 3 | its initialiser | - |

</details>

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
