---
title: "Phyre arrays: the PArray and PSharray containers, their ownership bit and the generated resize, copy and set-external bodies"
kind: "system"
category: "PhyreEngine"
addresses: "005B4E00, 005EFB10, 006065E0, 006045B0, 0063B9B0, 0062A870, 0060F400, 005C9740, 005C8BF0, 005C8CA0, 0060C3F0, 0060CC60, 006C7A40, 006C7D00, 00673130, 005AA3C0, 005DE950, 005C0090, 001C19A0, 001C2720, 0063DCA0, 005C4CC0"
---

## What the player sees

Nothing directly. Every list inside a loaded model, animation, material or shader, from the
channels of an animation clip to the shadow splits of a light, is one of these arrays. When a
`.phyre` file is loaded, its arrays can point straight into the file's data instead of owning a copy,
and the top bit of the count is what tells the engine not to free that memory.

## How it works

### Two containers

PhyreEngine has two array templates, both 16 bytes and both registered as reflected classes with
`m_count` at `+00`<sub>h</sub>:

- `PArray<T>` keeps its elements on the heap; `+08`<sub>h</sub> (`m_els`) is the pointer. The registration of
  `PArray<unsigned int,4>`, `005B4E00`, builds a `10`<sub>h</sub>-byte descriptor with alignment 8, an `m_count`
  member at 0 with the `WriteMask` annotation `7FFFFFFF`<sub>h</sub>, and an `m_els` array member (kind 2,
  element size 4) at 8.
- `PSharray<T>` keeps a single element inside the array: with a count of 1 the element is the
  8 bytes at `+08`<sub>h</sub> (`m_u`); with 0 there is no storage; with 2 or more `+08`<sub>h</sub> is the heap pointer.
  The registration of `PSharray<PUInt32>`, `005EFB10`, gives `m_u` attribute bit `40`<sub>h</sub>, the bit the
  reflection layer reads as "measured and defaulted inline".

Element access follows from this. `006045B0` returns the pointer at `+08`<sub>h</sub> of a `PArray`; `0063B9B0` returns the
address of `+08`<sub>h</sub> itself for a `PSharray` holding one element, null for none, and the stored pointer
otherwise.

### The ownership bit

Bit 31 of the count word marks storage the array does not own. The count is always read as
`m_count & 7FFFFFFFh` (`006065E0`, and the record hook `005C4CC0`). Every body that replaces the
storage frees the old block with `_aligned_free` (`00584730`) only when bit 31 is clear and the block
differs from the new one; a `PSharray` also never frees its inline slot.

Class destructors free
their array members the same way, owned storage only: `005AA160` two arrays at `+00`<sub>h</sub> and
`+10`<sub>h</sub>, `005AA2F0` three at `+100`<sub>h</sub>, `+110`<sub>h</sub> and `+120`<sub>h</sub> of a `138`<sub>h</sub>-byte record. Arrays of those
records are made with `new[]`: `005C9CF0` replaces one with a new array of `n` records (constructor
`005A9690`), and `005AA280` destroys one, calling `005AA2F0` on each record.

The set-external operation is the one that sets the bit. `0062A870` and `0060F400` refuse a count with
bit 31 already set (5), free owned old storage, store the new pointer and write `count | 80000000h`.
`00673130` and `006AF760` do the same on the array directly. The `PSharray` form `006C7D00` copies a
single element into the inline slot instead and leaves the count at a plain 1, so a one-element
`PSharray` always owns its element.

### Strings in arrays

A `PString` is one tagged pointer: bit 0 set marks text the string does not own. Copying a string
array (`001C19A0`) clears the tag, measures the text and duplicates it with alignment 2, so every copy
owns its text. `001C2720` frees each untagged string and then the block. `0063DCA0` releases a
`PSharray<PString>`'s old storage: a single inline string, or the whole owned block through `001C2720`.

`006A7800`, published by the `PString` registration `006A72B0`, points a string at foreign text: it
refuses an odd pointer with 5, frees the old text when it was owned and stores the pointer with bit 0
set (null stays null).

### The member records

The reflection layer reaches each array member through its member record, a
`PClassDataMemberPhyreArray<T>` or `PClassDataMemberPhyreSharray<T>`. The image holds 69 such vtables,
59 for `PArray` and 10 for `PSharray`. Each slot below first locates the array in the
object as the member's offset (`+48`<sub>h</sub>) minus the owning descriptor's `+F4`<sub>h</sub>.

| Slot offset | Body | What it does |
|---|---|---|
| `20`<sub>h</sub> | `006065E0` in all 69 | the count, bit 31 masked off |
| `28`<sub>h</sub> | a thunk per element type, such as `005C9740` | resize to a count |
| `30`<sub>h</sub>, `38`<sub>h</sub> | `006045B0` (`PArray`), `0063B9B0` (`PSharray`) | the element pointer |
| `40`<sub>h</sub> | `0062A870` (18 vtables), `0060F400` (22), `006A5A90` (6), others | set external storage |

The 50 distinct `+28`<sub>h</sub> slot bodies hold the per-type code: 46 jump to a separate resize body and 4 resize inline.
One body can serve several element types; `0060C3F0` is the resize of all 14 `PArray` vtables whose
element is a pointer, and `006C7A40` that of the 6 pointer `PSharray` vtables.

`m_els` and `m_u` are registered as `PClassDataMemberArrayDynamic<T>` records, which carry more
hooks: `+60`<sub>h</sub> reads the count (`005C4CC0`, in both registrations above), `+68`<sub>h</sub> returns the
element pointer for a `PSharray` (`00671250`; 0 in the `PArray` record) and `+70`<sub>h</sub> sets external
storage (`00673130` for `PArray<unsigned int,4>`, `0060F2D0` for `PSharray<PUInt32>`).

### Resizing

Every resize body has the same shape, shown by `005C8BF0` (`PArray<float>`):

1. When the new count equals the whole count word it returns 0 at once. An array with bit 31 set never
   matches, so resizing it always makes an owned copy.
2. It allocates the new count of elements through `0017D260` with the element type's alignment and
   copies the first `min(old, new)` elements; for element types with a default the helper fills the
   rest (for `PShadowSplit`, `006C2320` sets two fields to 10.0).
3. A failed allocation for a non-zero count returns `D`<sub>h</sub> with the array unchanged.
4. It frees the old storage when owned, through an element destructor for types that own memory
   (`005B7E10` frees the string of each `PAnimationChannelTarget`), and stores the pointer and the
   new count with bit 31 clear.

`PSharray` resizes (`0060CC60`) use the inline slot for a count of 1 and otherwise behave the same.
`0060C6C0` resizes a `PArray` of `18`<sub>h</sub>-byte elements outside the member records: `005E3380`
allocates the new block (alignment 8) and copies the kept elements, and a failed allocation returns
`D`<sub>h</sub>.

### Copying and appending

- Copy-assign builds owned storage for the source's count and copies into it, then frees the old
  storage when owned: `005AA3C0` (`PArray` of 4-byte elements), `005DE950` (`PSharray`). The count it
  stores has bit 31 clear, so the copy owns its elements even when the source did not.
- `006C5020` is the `PSharray` copy constructor: it zeroes the count before the copy-assign.
- `005C0090` appends one `{qword, dword}` element to the `PArray` at `+100`<sub>h</sub> of its object by
  reallocating with one more element; it returns 0 when the allocation fails, 1 otherwise.

## Layouts

PArray<T> (`10`<sub>h</sub>):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u32` | m_count | element count in bits 0-30; bit 31 = storage not owned |
| `08`<sub>h</sub> | `void*` | m_els | elements, or null |

PSharray<T> (`10`<sub>h</sub>):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u32` | m_count | as above |
| `08`<sub>h</sub> | `u64` | m_u | count 0: unused; count 1: the element itself; count 2+: pointer to elements |

PString (8):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `void*` | text; bit 0 = not owned |  |

PClassDataMemberArrayDynamic<T>, beyond the PClassDataMemberArray fields:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `60`<sub>h</sub> | `void*` | count hook (005C4CC0) |  |
| `68`<sub>h</sub> | `void*` | element-pointer hook: 00671250 for PSharray<PUInt32>, 0 for PArray<unsigned int,4> |  |
| `70`<sub>h</sub> | `void*` | set-external hook |  |

## Shipped data

| Fact | Value |
|---|---|
| `PClassDataMemberPhyreArray<T>` vtables | 59 |
| `PClassDataMemberPhyreSharray<T>` vtables | 10 |
| distinct `+28`<sub>h</sub> slot bodies | 50: 46 jump to a resize body, 4 resize inline |
| slot `+20`<sub>h</sub> | `006065E0` in all 69 |

### Data files

| File | Rows | What it lists |
|---|---:|---|
| [phyre-arrays-member-vtables.tsv](phyre-arrays-member-vtables.tsv) | 69 | each array member-record vtable: element type, slot `+28`<sub>h</sub> thunk and resize body, slots `+20`<sub>h</sub>, `+30`<sub>h</sub>, `+40`<sub>h</sub> |
| [phyre-arrays-template-bodies.tsv](phyre-arrays-template-bodies.tsv) | 79 | template bodies: resizes, allocate-and-copy helpers, element copiers and defaulters, copy-assigns, set-external, clear and destroy bodies, with their element types |

## Operations

- Count: `m_count & 7FFFFFFFh`, or member slot `+20`<sub>h</sub>.
- Elements: member slot `+30`<sub>h</sub>; for a `PSharray` with one element, the address of `+08`<sub>h</sub>.
- Resize: member slot `+28h(record, object, count)`; 0, or `D`<sub>h</sub> when out of memory.
- Point at foreign memory: member slot `+40h(record, object, pointer, count)`; 5 for a count with
  bit 31 set.

## Modding notes

- To make an array use memory you manage, store the pointer and `count | 80000000h`; the engine then
  never frees it. Resizing or copy-assigning such an array gives an owned copy.
- A `PSharray` with one element keeps it inside the array, so code that walks the elements must take
  the address of `+08`<sub>h</sub> rather than read it as a pointer.
- Strings copied into arrays always become owned copies; a tagged (bit 0) string is never freed.

## Related

- [Phyre reflection](phyre-reflection.md): member records, array kinds and the `+F4`<sub>h</sub> adjustment the slots use.
- [Phyre field schema](phyre-field-schema.md): how a file's array members map to these records.
- [Phyre asset files](phyre-asset-files.md): the cluster data the arrays are filled from.
- [Memory and allocation](../Compiler-And-C-Runtime/memory-and-allocation.md): `0017D260` and `00584730`.
