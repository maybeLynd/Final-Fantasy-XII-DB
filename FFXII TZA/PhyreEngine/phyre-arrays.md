[Home](../../README.md) / [PhyreEngine](README.md) / Phyre arrays

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Phyre arrays: the PArray and PSharray containers, their ownership bit and the generated resize, copy and set-external bodies | system | PhyreEngine | Engine framework | How PhyreEngine stores its reflected arrays: the 16-byte PArray&lt;T&gt; and the PSharray&lt;T&gt; whose size follows its inline element, both with a count word whose top bit marks storage the array does not own, the PString tagged pointer, the member-record vtables through which the reflection layer counts, resizes and repoints an array, and the per-element-type template bodies the compiler generated for them. | 0x005B4E00, 0x005EFB10, 0x006065E0, 0x006045B0, 0x0063B9B0, 0x0062A870, 0x0060F400, 0x005C9740, 0x005C8BF0, 0x005C8CA0, 0x0060C3F0, 0x0060CC60, 0x006C7A40, 0x006C7D00, 0x00673130, 0x005AA3C0, 0x005DE950, 0x005C0090, 0x001C19A0, 0x001C2720, 0x0063DCA0, 0x005C4CC0 |

## What the player sees

Nothing directly. Every list inside a loaded model, animation, material or shader, from the
channels of an animation clip to the shadow splits of a light, is one of these arrays. When a
`.phyre` file is loaded, its arrays can point straight into the file's data instead of owning a copy,
and the top bit of the count is what tells the engine not to free that memory.

## How it works

### Two containers

PhyreEngine has two array templates, both registered as reflected classes with `m_count` at `+0x00`:

- `PArray<T>` is 16 bytes and keeps its elements on the heap; `+0x08` (`m_els`) is the pointer. The registration of
  `PArray<unsigned int,4>`, `0x005B4E00`, builds a `0x10`-byte descriptor with alignment 8, an `m_count`
  member at 0 with the `WriteMask` annotation `0x7FFFFFFF`, and an `m_els` array member (kind 2,
  element size 4) at 8.
- `PSharray<T>` keeps a single element inside the array: with a count of 1 the element itself is
  stored from `+0x08` (`m_u`); with 0 there is no storage; with 2 or more `+0x08` is the heap pointer.
  Its size is `8 + max(8, element size)` bytes, 8 plus the larger of 8 and the element size, which the class
  registrations pass
  to `0x00632D80`:
  - `0x10` for `PSharray<PUInt32>` (`0x005EFBA9`) and the six pointer instantiations (`0x005B7B59`,
    `0x005EFEF9`, `0x0066A4F9`, `0x006989C9`, `0x006A8559`, `0x006C65F9`);
  - `0x50` for `PSharray<PDataBlockBufferD3D11>` (`0x0066A849`) and
    `PSharray<PIndexDataBlockBufferD3D11>` (`0x0066AB99`), whose `0x48`-byte elements (`0x00661CC0`,
    `0x00662170`) fill `+0x08` to `+0x4F` at a count of 1;
  - in `PDataBlockD3D11` the member `m_buffers` at `+0x20` (`0x006658F3`) is followed by
    `m_offsetInVertexBuffer` at `+0x70` (`0x006659E6`), and in `PIndexDataBlockD3D11` `m_buffers` at
    `+0x18` (`0x00666403`) is followed by `m_offsetInIndexBuffer` at `+0x68` (`0x006664F6`).

The registrations of `PSharray<PUInt32>` (`0x005EFD0A`), `PSharray<PDataBlockBufferD3D11>` (`0x0066A9A9`) and
`PSharray<PIndexDataBlockBufferD3D11>` (`0x0066ACF9`) give `m_u` attribute bit `0x40`, the bit the reflection
layer reads as "measured and defaulted inline".

Element access follows from this. `0x006045B0` returns the pointer at `+0x08` of a `PArray`; `0x0063B9B0` returns the
address of `+0x08` itself for a `PSharray` holding one element, null for no element, and the stored pointer
otherwise.

### The ownership bit

Bit `0x80000000` of the count word marks storage the array does not own. The count is always read as
`m_count & 0x7FFFFFFF` (`0x006065E0`, and the record hook `0x005C4CC0`). Every body that replaces the
storage frees the old block with `_aligned_free` (`0x00584730`) only when bit `0x80000000` is clear and the block
differs from the new one; a `PSharray` also never frees its inline slot.

Class destructors free
their array members the same way, owned storage only: `0x005AA160` two arrays at `+0x00` and
`+0x10`, `0x005AA2F0` three at `+0x100`, `+0x110` and `+0x120` of a `0x138`-byte record. Arrays of those
records are made with `new[]`: `0x005C9CF0` replaces one with a new array of `n` records (constructor
`0x005A9690`), and `0x005AA280` destroys one, calling `0x005AA2F0` on each record.

The set-external operation is the one that sets the bit. `0x0062A870` and `0x0060F400` refuse a count with
bit `0x80000000` already set (5), free owned old storage, store the new pointer and write `count | 0x80000000`.
They return 5 for the refused count (`0x0062A89D`, `0x0060F42D`) and 0 otherwise (`0x0062A8DD`, `0x0060F46D`).

`0x00673130` and `0x006AF760` do the same on the array directly, taking the array, the pointer and the count,
except that a count with bit `0x80000000` set returns 0, not 5, and leaves the array unchanged (`0x0067314B`,
`0x006AF77B`). Every other count returns 0 as well (`0x0067317A`, `0x006AF7AA`).

The `PSharray` forms copy a single element into the inline slot instead and leave the count at a plain 1, so a
one-element `PSharray` always owns its element:

- `0x006C7D00` copies one dword for `PSharray<PUInt32>` (`0x006C7D62`-`0x006C7D64`); it refuses a count with bit
  `0x80000000` set with 5 (`0x006C7D15`), and any count other than 1 gets the pointer and `count | 0x80000000`
  (`0x006C7D4F`, `0x006C7D96`, `0x006C7DA0`);
- `0x006A5950` copies one qword for the six pointer instantiations (`0x006A59B2`-`0x006A59B5`);
- `0x00672F30` and `0x00673030` copy the `0x48`-byte buffer records and store the record's own
  `TAsyncUpdate` vtable at `+0x28` (`0x00672F92`-`0x00672FD3`, `0x00673092`-`0x006730D3`);
- `0x0063DE10` stores the copy of the string made by `0x001C26B0` (`0x0063DE98`-`0x0063DEAA`).

### Strings in arrays

A `PString` is one tagged pointer: bit `0x1` set marks text the string does not own. Copying a string array
(`0x001C19A0`) clears the tag, measures the text and duplicates it with alignment 2, so every copy owns its text: a
block of the length plus one from `0x0017D260(length + 1, 2)`, filled with `memcpy` (`0x00861EBA`, `0x001C1A2C`) from the
text and its terminator. A null text, or a failed allocation, gives a null copy (`0x001C19F4`, `0x001C1A21`). `0x001C2720`
frees each untagged string and then the block.

`0x001C2720(block, count)` returns at once for a null block (`0x001C2723`), skips null strings (`0x001C2756`) and
frees the block last through `0x00584730` (`0x001C2773`).

`0x0063DCA0` releases a `PSharray<PString>`'s old storage: a single inline string, or the whole owned block through
`0x001C2720`. Its arguments are the array, the new elements, the new count, the old elements and the old count.
Nothing is freed when the old elements are the new ones (`0x0063DCCE`). An inline old string has its text freed
when it is non-null with bit `0x1` clear, whatever the array's bit `0x80000000` (`0x0063DCD5`-`0x0063DCE5`); an old
block goes to `0x001C2720(old elements, old count)` only when bit `0x80000000` of the array's count is clear
(`0x0063DCED`-`0x0063DCFF`).

It then stores the new count as given (`0x0063DD04`) and writes the new pointer to `+0x08` unless the new
elements are the inline slot (`0x0063DD06`-`0x0063DD0B`).

`0x006A7800`, published by the `PString` registration `0x006A72B0`, points a string at foreign text: it
refuses an odd pointer with 5, frees the old text when it was owned and stores the pointer with bit `0x1`
set (null stays null).

### The member records

The reflection layer reaches each array member through its member record, a
`PClassDataMemberPhyreArray<T>` or `PClassDataMemberPhyreSharray<T>`. The image holds 69 such vtables,
59 for `PArray` and 10 for `PSharray`. Each slot below first locates the array in the
object as the member's offset (`+0x48`) minus the owning descriptor's `+0xF4`.

| Slot offset | Body | What it does |
|---|---|---|
| `+0x20` | `0x006065E0` in all 69 | the count, bit `0x80000000` masked off |
| `+0x28` | a thunk per element type, such as `0x005C9740` | resize to a count |
| `+0x30`, `+0x38` | `0x006045B0` (`PArray`), `0x0063B9B0` (`PSharray`) | the element pointer |
| `+0x40` | `0x0062A870` (18 vtables), `0x0060F400` (22), `0x006A5A90` (6), others | set external storage |

The 50 distinct `+0x28` slot bodies hold the per-type code: 46 jump to a separate resize body and 4 resize inline.
One body can serve several element types; `0x0060C3F0` is the resize of all 14 `PArray` vtables whose
element is a pointer, and `0x006C7A40` that of the 6 pointer `PSharray` vtables.

`m_els` and `m_u` are registered as `PClassDataMemberArrayDynamic<T>` records, which carry more
hooks: `+0x60` reads the count (`0x005C4CC0`, in both registrations above), `+0x68` returns the
element pointer for a `PSharray` (`0x00671250`; 0 in the `PArray` record) and `+0x70` sets external
storage (`0x00673130` for `PArray<unsigned int,4>`, `0x0060F2D0` for `PSharray<PUInt32>`).

### Resizing

The resize bodies that keep their elements have the same shape, shown by `0x005C8BF0` (`PArray<float>`).
One helper keeps none: `0x001EF1A0`, for a `PSharray` of 8-byte elements (called from `0x001EE1D0`), zeroes
the new storage (`0x001EF212`-`0x001EF21A`) instead of copying, returns `0xD` when the allocation fails
(`0x001EF225`), and frees the old storage when owned. The common shape:

1. When the new count equals the whole count word it returns 0 at once (`0x005C8C15`-`0x005C8C17`). An array with
   bit `0x80000000` set never matches, so resizing it always makes an owned copy.
2. It allocates the new count of elements through `0x0017D260` with the element type's alignment and
   copies the first `min(old, new)` elements; for element types with a default the helper fills the
   rest (for `PShadowSplit`, `0x006C2320` sets two fields to 10.0). `0x005C8BF0` asks for `count * 4` bytes
   with alignment 4 (`0x005C8C23`-`0x005C8C2C`) and copies with `0x005A5B40` (`0x005C8C47`).
3. A failed allocation for a non-zero count returns `0xD` with the array unchanged (`0x005C8C8D`-`0x005C8C96`). A
   new count of 0 allocates nothing (`0x005C8C21`) and goes on to step 4 with a null pointer, so the array ends
   empty with its owned storage freed.
4. It frees the old storage when owned, through an element destructor for types that own memory
   (`0x005B7E10` frees the string of each `PAnimationChannelTarget`), and stores the pointer and the
   new count with bit `0x80000000` clear (`0x005C8C4C`-`0x005C8C6E`), then returns 0 (`0x005C8C70`). Old storage
   equal to the new block, or null, is never freed (`0x005C8C53`, `0x005C8C63`).

The `PAnimationChannelTarget` resize `0x005C8CA0` gets its new block from `0x005AD2B0`, which asks for
`count * 0x38` bytes with alignment 8, copies the kept elements with `0x005A5BD0` and defaults the rest with
`0x005BED40` (`0x005AD2CB`-`0x005AD2FF`). For owned old storage it calls `0x005B7E10` with the old count
(`0x005C8D07`-`0x005C8D0B`), which frees the text at `+0x28` of each element when that pointer is non-null with bit
`0x1` clear, then the block (`0x005B7E40`-`0x005B7E63`); a null block returns at once (`0x005B7E13`).

`PSharray` resizes (`0x0060CC60`) use the inline slot for a count of 1 and otherwise behave the same.
`0x0060C6C0` resizes a `PArray` of `0x18`-byte elements outside the member records: `0x005E3380`
allocates the new block (alignment 8) and copies the kept elements, and a failed allocation returns
`0xD`.

### Copying and appending

- Copy-assign builds owned storage for the source's count and copies into it, then frees the old
  storage when owned: `0x005AA3C0` (`PArray` of 4-byte elements), `0x005DE950` (`PSharray`). The count it
  stores has bit `0x80000000` clear, so the copy owns its elements even when the source did not.
- `0x005AA3C0` asks `0x0017D260` for `count * 4` bytes with alignment 4 and copies with `0x005A5B40`
  (`0x005AA3EA`-`0x005AA409`). A source count of 0, or a failed allocation, leaves the new pointer null, and the
  source's count is stored all the same (`0x005AA434`-`0x005AA43B`), so a failed allocation gives an array with that
  count and a null `m_els`.
- `0x005DE950` reads the source's elements from the inline slot for a count of 1, through the pointer for 2 or
  more, and as null for 0 (`0x005DE976`-`0x005DE987`). `0x005FEE80` gives the new storage: the destination's own
  `+0x08` for a count of 1, `count * 4` bytes at alignment 4 for 2 or more (`0x005FEEA4`-`0x005FEEB5`), with each
  element copied as a dword (`0x005FEED0`-`0x005FEEE2`).
- As in `0x005AA3C0`, a failed allocation in `0x005DE950` stores the source's count with a null pointer (`0x005FEEBD`,
  `0x005DE9D2`-`0x005DE9DC`). It frees old storage only when it is neither the new storage nor the inline slot
  (`0x005DE9B4`-`0x005DE9CD`), and writes the pointer only when the new storage is not the inline slot
  (`0x005DE9D7`). Both copy-assigns return the destination (`0x005AA431`, `0x005DE9D4`).
- `0x005DE950` reads the destination's old count and old pointer after the copy (`0x005DE992`, `0x005DE9A6`, after
  the call at `0x005DE98D`). For a source count of 1, `0x005FEE80` has by then stored the element in the
  destination's `+0x08` (`0x005FEE8F`, `0x005FEEDC`-`0x005FEEE2`). A destination that held 2 or more owned elements
  therefore hands `0x00584730` its old pointer with the low 32 bits replaced by that element (`0x005DE9CD`), not
  the old block.
- `0x006C5020` is the `PSharray` copy constructor: it zeroes the count before the copy-assign.
- `0x005C0090` appends one `{qword, dword}` element to the `PArray` at `+0x100` of its object by
  reallocating with one more element; it returns 0 when the allocation fails, 1 otherwise. It asks
  `0x0017D260` for `((count & 0x7FFFFFFF) + 1) * 0x10` bytes with alignment 8 (`0x005C00A2`-`0x005C00BC`); a failed
  allocation returns 0 with the array unchanged (`0x005C00C9`-`0x005C00DD`).
- On success `0x005C0090` copies the old 16-byte elements (`0x005C0100`-`0x005C0113`) and writes the qword argument
  at `+0x0` and the dword argument at `+0x8` of the new last element (`0x005C0127`-`0x005C012C`). It frees owned
  old storage that is not null (`0x005C013C`-`0x005C014F`), stores the block at `+0x108` and
  `(count & 0x7FFFFFFF) + 1` at `+0x100` (`0x005C0154`-`0x005C0163`), so the bit `0x80000000` is clear, and
  returns 1 (`0x005C0169`-`0x005C0172`).

## Layouts

### Reflected members

The members below are the ones the code of this page's classes uses or the reflection registers; each registered member is named by its registration (the registering function, through 0x00632960), and each class fence covers only those members.

`PArray` (`0x10` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | m_count | element count in the bits under mask `0x7FFFFFFF`; bit `0x80000000` = storage not owned; m_count (u32), registered by `0x005B5460` (`0x00632960` at `0x005B55FA`); shipped files name each instantiation, such as PArray&lt;PAnimationChannel *&gt;, each registered by its own template descriptor; the member getter `0x006065E0` returns it with bit `0x80000000` cleared (`0x006065F3`) |

`PShadowSplit` (`0xE8` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[192]` | bytes00 | `+0x0` to `+0xBF`; no registered member covers it (`0x006C0E00` registers the `0xE8`-byte class at `0x006C0E50`) |
| `+0xCC` | `u8[4]` | bytesCC | the four bytes after m_farPlane (`+0xC8`): the placement constructor `0x006C0A80` writes 10.0 to m_farPlane and 0 here with one qword store (`0x006C0A87`); no registered member covers it (`0x006C0E00` registers the `0xE8`-byte class at `0x006C0E50`) |
| `+0xE4` | `u8[4]` | bytesE4 | the bytes after the dword the placement constructor `0x006C0A80` clears at `+0xE0` (`0x006C0AAB`) up to the end of the `0xE8`-byte class; no registered member covers it (`0x006C0E00` registers the `0xE8`-byte class at `0x006C0E50`) |

### Array and string headers

The structures below are the ones the mechanisms above use.

PArray&lt;T&gt; (`0x10`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | m_count | element count in the bits under mask `0x7FFFFFFF`; bit `0x80000000` = storage not owned |
| `+0x08` | `void*` | m_els | elements, or null |

PSharray&lt;T&gt; (8 + max(8, sizeof T): `0x10` up to 8-byte elements; `0x50` for PDataBlockBufferD3D11 and PIndexDataBlockBufferD3D11):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | m_count | as above |
| `+0x08` | `...` | m_u | the element of type T or a pointer: count 0: unused; count 1: the element itself, max(8, sizeof T) bytes; count 2+: pointer to elements |

PString (8):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` |  | text; bit `0x1` = not owned |

PClassDataMemberArrayDynamic&lt;T&gt;, beyond the PClassDataMemberArray fields:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x60` | `void*` |  | count hook (`0x005C4CC0`) |
| `+0x68` | `void*` |  | element-pointer hook: `0x00671250` for PSharray&lt;PUInt32&gt;, 0 for PArray&lt;unsigned int,4&gt; |
| `+0x70` | `void*` |  | set-external hook |

## Shipped data

| Fact | Value |
|---|---|
| `PClassDataMemberPhyreArray<T>` vtables | 59 |
| `PClassDataMemberPhyreSharray<T>` vtables | 10 |
| distinct `+0x28` slot bodies | 50: 46 jump to a resize body, 4 resize inline |
| slot `+0x20` | `0x006065E0` in all 69 |

### Data files

| File | Rows | What it lists |
|---|---:|---|
| [phyre-arrays-member-vtables.tsv](phyre-arrays-member-vtables.tsv) | 69 | each array member-record vtable: element type, slot `+0x28` thunk and resize body, slots `+0x20`, `+0x30`, `+0x40` |
| [phyre-arrays-template-bodies.tsv](phyre-arrays-template-bodies.tsv) | 85 | template bodies: resizes, allocate-and-copy helpers, element copiers and defaulters, copy-assigns, set-external, clear and destroy bodies, with their element types |

## Operations

- Count: `m_count & 0x7FFFFFFF`, or member slot `+0x20`.
- Elements: member slot `+0x30`; for a `PSharray` with one element, the address of `+0x08`.
- Resize: member slot `+0x28(record, object, count)`; 0, or `0xD` when out of memory.
- Point at foreign memory: member slot `+0x40(record, object, pointer, count)`; 5 for a count with
  bit `0x80000000` set.

## Modding notes

- To make an array use memory you manage, store the pointer and `count | 0x80000000`; the engine then
  never frees it. A `PSharray` takes foreign memory only for two or more elements: for a count of 1
  `0x0063B9B0` returns the address of `+0x08` (`0x0063B9D3`), and every set-external body copies the single
  element there. Resizing or copy-assigning such an array gives an owned copy.
- A `PSharray` with one element keeps it inside the array, so code that walks the elements must take
  the address of `+0x08` rather than read it as a pointer.
- Strings copied into arrays always become owned copies; a tagged (bit `0x1`) string is never freed.

## Related

- [Phyre reflection](phyre-reflection.md): member records, array kinds and the `+0xF4` adjustment the slots use.
- [Phyre field schema](phyre-field-schema.md): how a file's array members map to these records.
- [Phyre asset files](phyre-asset-files.md): the cluster data the arrays are filled from.
- [Memory and allocation](../Compiler-And-C-Runtime/memory-and-allocation.md): `0x0017D260` and `0x00584730`.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Resource: `0x001C26B0` is called by `0x00597970`, `0x00597A70`, `0x0059ED70`, `0x0059EE10`; those functions are documented on
  [file path resolution](../Game-Files-And-Data-Tables/file-path-resolution.md).
