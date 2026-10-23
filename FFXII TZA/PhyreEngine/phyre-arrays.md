---
title: "Phyre arrays: the PArray and PSharray containers, their ownership bit and the generated resize, copy and set-external bodies"
kind: "system"
category: "PhyreEngine"
addresses: "0x005B4E00, 0x005EFB10, 0x006065E0, 0x006045B0, 0x0063B9B0, 0x0062A870, 0x0060F400, 0x005C9740, 0x005C8BF0, 0x005C8CA0, 0x0060C3F0, 0x0060CC60, 0x006C7A40, 0x006C7D00, 0x00673130, 0x005AA3C0, 0x005DE950, 0x005C0090, 0x001C19A0, 0x001C2720, 0x0063DCA0, 0x005C4CC0"
---

## What the player sees

Nothing directly. Every list inside a loaded model, animation, material or shader, from the
channels of an animation clip to the shadow splits of a light, is one of these arrays. When a
`.phyre` file is loaded, its arrays can point straight into the file's data instead of owning a copy,
and the top bit of the count is what tells the engine not to free that memory.

## How it works

### Two containers

PhyreEngine has two array templates, both 16 bytes and both registered as reflected classes with
`m_count` at `+0x00`:

- `PArray<T>` keeps its elements on the heap; `+0x08` (`m_els`) is the pointer. The registration of
  `PArray<unsigned int,4>`, `0x005B4E00`, builds a `0x10`-byte descriptor with alignment 8, an `m_count`
  member at 0 with the `WriteMask` annotation `0x7FFFFFFF`, and an `m_els` array member (kind 2,
  element size 4) at 8.
- `PSharray<T>` keeps a single element inside the array: with a count of 1 the element is the
  8 bytes at `+0x08` (`m_u`); with 0 there is no storage; with 2 or more `+0x08` is the heap pointer.
  The registration of `PSharray<PUInt32>`, `0x005EFB10`, gives `m_u` attribute bit `0x40`, the bit the
  reflection layer reads as "measured and defaulted inline".

Element access follows from this. `0x006045B0` returns the pointer at `+0x08` of a `PArray`; `0x0063B9B0` returns the
address of `+0x08` itself for a `PSharray` holding one element, null for none, and the stored pointer
otherwise.

### The ownership bit

Bit 31 of the count word marks storage the array does not own. The count is always read as
`m_count & 0x7FFFFFFF` (`0x006065E0`, and the record hook `0x005C4CC0`). Every body that replaces the
storage frees the old block with `_aligned_free` (`0x00584730`) only when bit 31 is clear and the block
differs from the new one; a `PSharray` also never frees its inline slot.

Class destructors free
their array members the same way, owned storage only: `0x005AA160` two arrays at `+0x00` and
`+0x10`, `0x005AA2F0` three at `+0x100`, `+0x110` and `+0x120` of a `0x138`-byte record. Arrays of those
records are made with `new[]`: `0x005C9CF0` replaces one with a new array of `n` records (constructor
`0x005A9690`), and `0x005AA280` destroys one, calling `0x005AA2F0` on each record.

The set-external operation is the one that sets the bit. `0x0062A870` and `0x0060F400` refuse a count with
bit 31 already set (5), free owned old storage, store the new pointer and write `count | 0x80000000`.
`0x00673130` and `0x006AF760` do the same on the array directly. The `PSharray` form `0x006C7D00` copies a
single element into the inline slot instead and leaves the count at a plain 1, so a one-element
`PSharray` always owns its element.

### Strings in arrays

A `PString` is one tagged pointer: bit 0 set marks text the string does not own. Copying a string
array (`0x001C19A0`) clears the tag, measures the text and duplicates it with alignment 2, so every copy
owns its text. `0x001C2720` frees each untagged string and then the block. `0x0063DCA0` releases a
`PSharray<PString>`'s old storage: a single inline string, or the whole owned block through `0x001C2720`.

`0x006A7800`, published by the `PString` registration `0x006A72B0`, points a string at foreign text: it
refuses an odd pointer with 5, frees the old text when it was owned and stores the pointer with bit 0
set (null stays null).

### The member records

The reflection layer reaches each array member through its member record, a
`PClassDataMemberPhyreArray<T>` or `PClassDataMemberPhyreSharray<T>`. The image holds 69 such vtables,
59 for `PArray` and 10 for `PSharray`. Each slot below first locates the array in the
object as the member's offset (`+0x48`) minus the owning descriptor's `+0xF4`.

| Slot offset | Body | What it does |
|---|---|---|
| `+0x20` | `0x006065E0` in all 69 | the count, bit 31 masked off |
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

Every resize body has the same shape, shown by `0x005C8BF0` (`PArray<float>`):

1. When the new count equals the whole count word it returns 0 at once. An array with bit 31 set never
   matches, so resizing it always makes an owned copy.
2. It allocates the new count of elements through `0x0017D260` with the element type's alignment and
   copies the first `min(old, new)` elements; for element types with a default the helper fills the
   rest (for `PShadowSplit`, `0x006C2320` sets two fields to 10.0).
3. A failed allocation for a non-zero count returns `0xD` with the array unchanged.
4. It frees the old storage when owned, through an element destructor for types that own memory
   (`0x005B7E10` frees the string of each `PAnimationChannelTarget`), and stores the pointer and the
   new count with bit 31 clear.

`PSharray` resizes (`0x0060CC60`) use the inline slot for a count of 1 and otherwise behave the same.
`0x0060C6C0` resizes a `PArray` of `0x18`-byte elements outside the member records: `0x005E3380`
allocates the new block (alignment 8) and copies the kept elements, and a failed allocation returns
`0xD`.

### Copying and appending

- Copy-assign builds owned storage for the source's count and copies into it, then frees the old
  storage when owned: `0x005AA3C0` (`PArray` of 4-byte elements), `0x005DE950` (`PSharray`). The count it
  stores has bit 31 clear, so the copy owns its elements even when the source did not.
- `0x006C5020` is the `PSharray` copy constructor: it zeroes the count before the copy-assign.
- `0x005C0090` appends one `{qword, dword}` element to the `PArray` at `+0x100` of its object by
  reallocating with one more element; it returns 0 when the allocation fails, 1 otherwise.

## Layouts

### Reflected members

The members below are the ones the code of this page's classes uses or the reflection registers; each registered member is named by its registration (the registering function, through 0x00632960), and each class fence covers only those members.

```python
+0x00    u32             m_count                element count in bits 0-30; bit 31 = storage not owned; m_count (u32), registered by 0x005B5460 (0x00632960 at 0x005B55FA); shipped files name each instantiation, such as PArray<PAnimationChannel *>, each registered by its own template descriptor; the member getter 0x006065E0 returns it with bit 31 cleared (0x006065F3)
```

```struct PShadowSplit base=record size=0xE8
+0x00    u8[192]         bytes00                +0x0 to +0xBF; no registered member covers it (0x006C0E00 registers the
                                                0xE8-byte class at 0x006C0E50)
+0xCC    u8[4]           bytesCC                the four bytes after m_farPlane (+0xC8): the placement constructor
                                                0x006C0A80 writes 10.0 to m_farPlane and 0 here with one qword store
                                                (0x006C0A87); no registered member covers it (0x006C0E00 registers the
                                                0xE8-byte class at 0x006C0E50)
+0xE4    u8[4]           bytesE4                the bytes after the dword the placement constructor 0x006C0A80 clears
                                                at +0xE0 (0x006C0AAB) up to the end of the 0xE8-byte class; no registered
                                                member covers it (0x006C0E00 registers the 0xE8-byte class at 0x006C0E50)
```

### Array and string headers

The structures below are the ones the mechanisms above use.

PArray&lt;T&gt; (`0x10`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | m_count | element count in bits 0-30; bit 31 = storage not owned |
| `+0x08` | `void*` | m_els | elements, or null |

PSharray&lt;T&gt; (`0x10`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | m_count | as above |
| `+0x08` | `u64` | m_u | count 0: unused; count 1: the element itself; count 2+: pointer to elements |

PString (8):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | text; bit 0 = not owned |  |

PClassDataMemberArrayDynamic&lt;T&gt;, beyond the PClassDataMemberArray fields:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x60` | `void*` | count hook (0x005C4CC0) |  |
| `+0x68` | `void*` | element-pointer hook: 0x00671250 for PSharray&lt;PUInt32&gt;, 0 for PArray&lt;unsigned int,4&gt; |  |
| `+0x70` | `void*` | set-external hook |  |

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
| [phyre-arrays-template-bodies.tsv](phyre-arrays-template-bodies.tsv) | 79 | template bodies: resizes, allocate-and-copy helpers, element copiers and defaulters, copy-assigns, set-external, clear and destroy bodies, with their element types |

## Operations

- Count: `m_count & 0x7FFFFFFF`, or member slot `+0x20`.
- Elements: member slot `+0x30`; for a `PSharray` with one element, the address of `+0x08`.
- Resize: member slot `+0x28(record, object, count)`; 0, or `0xD` when out of memory.
- Point at foreign memory: member slot `+0x40(record, object, pointer, count)`; 5 for a count with
  bit 31 set.

## Modding notes

- To make an array use memory you manage, store the pointer and `count | 0x80000000`; the engine then
  never frees it. Resizing or copy-assigning such an array gives an owned copy.
- A `PSharray` with one element keeps it inside the array, so code that walks the elements must take
  the address of `+0x08` rather than read it as a pointer.
- Strings copied into arrays always become owned copies; a tagged (bit 0) string is never freed.

## Related

- [Phyre reflection](phyre-reflection.md): member records, array kinds and the `+0xF4` adjustment the slots use.
- [Phyre field schema](phyre-field-schema.md): how a file's array members map to these records.
- [Phyre asset files](phyre-asset-files.md): the cluster data the arrays are filled from.
- [Memory and allocation](../Compiler-And-C-Runtime/memory-and-allocation.md): `0x0017D260` and `0x00584730`.
