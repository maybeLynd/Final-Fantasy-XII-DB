---
title: "Object construction and destruction: vtable installs, deleting destructors, deallocators and owned buffers"
kind: "system"
category: "Compiler and C runtime"
addresses: "0x00809950, 0x00210EB0, 0x0019C590, 0x00584730, 0x0019C570, 0x0016D6A0, 0x007AD450, 0x0085E710, 0x00210EC0, 0x001D70A0, 0x00195530, 0x0086CE50, 0x01CD6268, 0x0015BC40, 0x00792350, 0x001EDF00, 0x005CA130, 0x00627750, 0x00623F50, 0x0019CA20, 0x001A4250"
---

## What the player sees

Nothing directly. Every character, effect, sound object and menu element is built and freed through
these few patterns, and a hook that breaks one of them shows up as a crash or a slow leak when objects
are created or destroyed, typically on area changes.

## How it works

### Constructors install vtables base first

A constructor stores a vtable with `lea reg, [vtable]; mov [object], reg`. A derived constructor calls
its base constructor, which stores the base vtable, and then overwrites it with its own. The C++ table
entry `0x0015BC40` shows both steps for the game's application object `0x01F7E350`: the base constructor
`0x00792350` stores `Phyre::PFramework::PApplication`'s vtable `0x01CB2508`, and `0x0015BC40` then stores
`GameApplication`'s vtable `0x008C5760` (`0x0015BC61`).

Every vtable is preceded by a pointer to its RTTI complete-object locator, so `vtable[-1]` names the
class; see [class hierarchy](../Engine-Core/class-hierarchy.md).

### The scalar deleting destructor

Slot 0 of a class with a virtual destructor is its scalar deleting destructor. It takes the object in
`rcx` and a flag in `edx`, destroys the object, frees it when bit `0x1` is set, and returns the object
in `rax`. The size it passes to the deallocator is the class size. The flag is tested where it arrives
or, when the destructor calls another function first, in the register it was saved to:

- `0x001D70A0` stores `ExtraUI`'s vtable, tests `dl, 1` (`0x001D70B3`) and calls `0x00809950` with
  `edx = 0x90`.
- `0x00195530` copies `edx` to `ebx` (`0x0019553A`), calls the inner destructor `0x00195180`, then tests
  `bl, 1` (`0x00195544`) and calls `0x00809950` with `edx = 0x98`.

`0x00809950` jumps to `0x00210EB0`, which jumps to `0x0019C590`, the `free` import stub; the size is ignored.

### The two-bit form

Most destructors test a second bit. `0x0086CE50` is the whole pattern:

1. Store the vtable, then test bit `0x1` (`0x0086CE6C`); when clear, return the object.
2. Test bit `0x4` (`0x0086CE71`).
3. Clear: call `0x00584730`, which is `if (p) _aligned_free(p)` (`0x0019C570` is the `_aligned_free` import
   stub).
4. Set: load the size (`edx = 0x28`) and call `0x0016D6A0`, which is `ret 0`.

A caller passing `0x5` therefore destroys the object and keeps its storage. Two other deallocators sit
on the bit-clear side: `0x007AD450` frees the block whose base is stored 8 bytes before the object,
through the function pointer at `0x02EAD0B8`, and `0x0085E710` counts the free in `0x02EAF6C8` and jumps
through the pointer at `0x01F44CF8`.

### Destructors rewind to the base vtable

The 26 vtables at `0x01CD6268`, one every `0x20` bytes, are `Phyre::PInputs::PInputSource` and its 25
subclasses; each one's own RTTI locator names it. Every slot-0 destructor stores the base vtable
`0x01CD6268` into the object before testing the flags, and then passes its own class's size to the
sized-delete call. A destructor's vtable store therefore names the class whose destructor runs next,
not the class it belongs to; the class comes from where the destructor's address sits.

| Vtable | Class | Destructor | Size |
|---|---|---|---|
| `0x01CD6268` | `PInputSource` | `0x0086CE50` | `0x28` |
| `0x01CD6288` | `PInputSourceKey` | `0x0086CF40` | `0x40` |
| `0x01CD62A8` | `PInputSourceJoypadButton` | `0x0086CEF0` | `0x40` |
| `0x01CD62C8` | `PInputSourceJoypadAxis` | `0x0086CEA0` | `0x38` |
| `0x01CD62E8` | `PInputSourceMouseButton` | `0x0086D2B0` | `0x38` |
| `0x01CD6308` | `PInputSourceMouseDeltaX` | `0x0086D300` | `0x40` |
| `0x01CD6328` | `PInputSourceMouseDeltaY` | `0x0086D350` | `0x40` |
| `0x01CD6348` | `PInputSourceTouchRotate` | `0x0086D490` | `0x28` |
| `0x01CD6368` | `PInputSourceTouchPinch` | `0x0086D440` | `0x28` |
| `0x01CD6388` | `PInputSourceTouchTwoFingerDragX` | `0x0086D4E0` | `0x28` |
| `0x01CD63A8` | `PInputSourceTouchTwoFingerDragY` | `0x0086D530` | `0x28` |
| `0x01CD63C8` | `PInputSourceTouchDragX` | `0x0086D3A0` | `0x28` |
| `0x01CD63E8` | `PInputSourceTouchDragY` | `0x0086D3F0` | `0x28` |
| `0x01CD6408` | `PInputSourceMotionQuatX` | `0x0086D1C0` | `0x28` |
| `0x01CD6428` | `PInputSourceMotionQuatY` | `0x0086D210` | `0x28` |
| `0x01CD6448` | `PInputSourceMotionQuatZ` | `0x0086D260` | `0x28` |
| `0x01CD6468` | `PInputSourceMotionQuatW` | `0x0086D170` | `0x28` |
| `0x01CD6488` | `PInputSourceMotionAngularVelocityX` | `0x0086CF90` | `0x28` |
| `0x01CD64A8` | `PInputSourceMotionAngularVelocityY` | `0x0086CFE0` | `0x28` |
| `0x01CD64C8` | `PInputSourceMotionAngularVelocityZ` | `0x0086D030` | `0x28` |
| `0x01CD64E8` | `PInputSourceMotionLinearAccelerationX` | `0x0086D080` | `0x28` |
| `0x01CD6508` | `PInputSourceMotionLinearAccelerationY` | `0x0086D0D0` | `0x28` |
| `0x01CD6528` | `PInputSourceMotionLinearAccelerationZ` | `0x0086D120` | `0x28` |
| `0x01CD6548` | `PInputSourceVisionTrackerX` | `0x0086D580` | `0x28` |
| `0x01CD6568` | `PInputSourceVisionTrackerY` | `0x0086D5D0` | `0x28` |
| `0x01CD6588` | `PInputSourceVisionTrackerZ` | `0x0086D620` | `0x28` |

Slot 2 of the base is `_purecall` (`0x00861EC6`) and every subclass fills it. Slot 1 of the base and of
the 19 touch, motion and vision-tracker classes is `0x0016D6A0`; the key, joypad and mouse classes fill it.

### Counted buffers with an ownership bit

Many records hold an array as two fields: a 32-bit count whose bit `0x80000000` marks storage the record
does not own, and a pointer. The release helpers free the pointer through `0x00584730` only when bit `0x80000000`
is clear and then zero both fields (`0x005DD620`, `0x00597B00`). A replace frees the old pointer under the
same test before storing the new one (`0x00672990`). `0x005CA130` stores a borrowed pointer and sets bit `0x80000000`
with the count.

`0x005CA130(record, pointer, count)` returns 5 and stores nothing when the count it is given already has bit
`0x80000000` set (`0x005CA148`-`0x005CA14D`). Otherwise, when the old pointer differs from the new one and bit
`0x80000000` of the old count is clear, it releases the old array with `0x005B7E10(old, oldCount & 0x7FFFFFFF)`
(`0x005CA162`-`0x005CA17C`). It then stores the pointer and `count | 0x80000000` and returns 0
(`0x005CA181`-`0x005CA190`).

`0x005B7E10` returns at once for a null array (`0x005B7E13`). Otherwise it frees, through `0x00584730`, the pointer
at `+0x28` of each `0x38`-byte element when that pointer is non-null with bit `0x1` clear, and then the array
itself (`0x005B7E40`-`0x005B7E63`).

In some records a count of 0 or 1 keeps the element inline in the pointer field: `0x00627750` and the
accessor `0x00623F50` use the field itself as the element when `count & 0x7FFFFFFF` is below 2, and
dereference it otherwise. A tagged-pointer variant marks borrowed storage with bit `0x1` of the pointer
instead (`0x005A17A0`).

Both functions handle `0x28`-byte elements. `0x00623F50(record, index)` reads the count at `+0x18` and the
field at `+0x20`. An index not below `count & 0x7FFFFFFF` returns 0 (`0x00623F5A`, `0x00623F8E`); any other index
returns the u64 at `+0x08` of element `index` (`0x00623F6A`-`0x00623F88`).

`0x00627750(record, count)` sets a new count, with the count word at `+0x00` and the field at `+0x08`. A count
equal to the whole stored word returns 0 at once (`0x0062776F`). Otherwise `0x0061CF20` gives the new storage: 0
for a count of 0, the field itself for a count of 1, and for a larger count a block of `count * 0x28` bytes
from `0x0017D260` called with `edx = 8`. It zeroes every element of the new storage (`0x0061CF2C`-`0x0061CF88`). The
old elements are not copied.

A failed allocation for a non-zero count returns 13 (`0x0062779E`). The old array is freed through `0x00584730`
when it is non-null, is neither the field itself nor the new storage, and bit `0x80000000` of the old count is
clear (`0x006277AC`-`0x006277C9`). The field then takes the new block unless the new storage is the field itself,
the count word takes the new count, and the call returns 0 (`0x006277CE`-`0x006277DD`).

### Allocator-owned containers

EASTL containers carry an allocator object whose vtable slot `+0x18` frees `(pointer, bytes)`.
`0x001EDF00` installs the `eastl::allocator_memory_log` vtable; containers pass it a name such as
`EASTL vector` or `EASTL set` (`0x0019C630`). A vector release calls the allocator with its buffer and
capacity in bytes (`0x0019CA20`); list clears walk the nodes and release each through the same slot
(`0x00199B00`).

`0x0019CA20` handles `0x18`-byte elements. It does nothing when the buffer at `+0x00` is null (`0x0019CA33`).
Otherwise it calls slot `+0x18` of the allocator at `+0x18` with the buffer and
`(capacityEnd - buffer) / 0x18 * 0x18` bytes, `capacityEnd` being the pointer at `+0x10`
(`0x0019CA38`-`0x0019CA6C`).

The compiler generates the container operations once per element type. 76 such bodies between
`0x00188640` and `0x001FFF00` are listed in [`object-construction-and-destruction-eastl-container-instances.tsv`](object-construction-and-destruction-eastl-container-instances.tsv)
with the operation and element size of each: vector reserve, insert, erase, copy, fill and release,
tree copy, erase and node creation, list insert and clear, and element copy constructors.

Two examples: `0x001AF000` inserts `n` copies into a vector of `0x40`-byte elements, growing the buffer to
the larger of twice the old count (1 when empty) and the new count, and `0x001BA990` erases a range of
`0x2A8`-byte `ChrModel` elements, destroying each through slot 0 of its vtable.

Five of them are destructors of one class template that pairs these containers with a lock:
`0x00199A80`, `0x0019C870`, `0x0019DAD0`, `0x001B3AF0` and `0x001E74F0`. Each destroys the PhyreEngine lock
record at `+0x90` (`0x28` bytes; see [runtime services](runtime-services.md)) through `0x005CD6D0`,
which closes the event at lock `+0x08`, when the byte at `+0xB8` is set. It then erases the trees at
`+0x58` and `+0x20` (`0x28`-byte nodes; `0x001E7560` for `0x001E74F0`) and frees the vector at `+0x00`,
whose elements are `0x10`, `0x18`, `0x118`, `0x20` and `0x10` bytes.

### Columns of object-construction-and-destruction-eastl-container-instances.tsv

| Column | Holds |
|---|---|
| `evidence` | what in the body shows it is EASTL container code, in a fixed order separated by semicolons: `allocator allocate slot` and `allocator free slot +0x18` for calls through the container allocator's vtable (slot `+0x10` allocates, `+0x18` frees), `0x001EDF00` with the allocator name it passes or `(copied allocator)` when it copies the source's allocator, and `calls` with the other container bodies it calls. A body with no such call is identified by the bodies it calls, the function that calls it (`called by`), or what its loop does. The most common value is `allocator free slot +0x18` alone (24 of the 76 rows) |

The template is the record pool that [game application](../Engine-Core/game-application.md)
describes: its constructor `0x001997F0` builds the lock at `+0x90` with `0x005CC8A0` and stores the
flag at `+0xB8`, and `0x00199A80` is the destructor that the unwind funclet `0x00896C60` of
`0x001999D0` runs on the `AsyncJobManager` pool at `+0x90`.

`0x001E74F0` is reached only from the unwind funclet `0x008985BE` of `0x001E71B0`. `0x001E76B0`, from the
unwind funclet `0x00898660` of `0x001E7480`, releases a vector of `0x3C`-byte elements: it divides the
byte span by 60 and multiplies by `0x3C`.

`0x00210EC0` is a one-argument allocation entry: it sets `r8d = -1` and `edx = 0` and
jumps to the `malloc` import stub `0x0085E730`; the lazy singleton `0x0018A620` allocates its object through it.

## Layouts

```python
scalar deleting destructor, as the call sites see it
  rcx = object
  edx = flags   0x1  free the storage
                0x4  sized delete (0x0016D6A0, frees nothing) instead of 0x00584730
  rax = object on return
```

Counted buffer, 16 bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | count | mask `0x7FFFFFFF` element count, bit `0x80000000` storage not owned |
| `+0x08` | `u64` | data | pointer; the element itself when the count is below 2 (inline form) |

PInputSource vtable, `0x20` bytes per class from `0x01CD6260`; the u64 at `-0x08` is the RTTI complete-object locator:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u64` | slot0 | scalar deleting destructor |
| `+0x08` | `u64` | slot1 |  |
| `+0x10` | `u64` | slot2 |  |

## Shipped data

| Fact | Value |
|---|---|
| deleting destructors | 1,937 functions, each counted once with its chained exception-table entries: each tests bit `0x1` of the incoming flag, in `edx` or in a register `edx` was copied to, with `test` followed by `je` or `jne`, and on the bit-set side calls `0x00809950`, `0x00210EB0`, `0x00584730`, `0x007AD450`, `0x0085E710` or `0x0016D6A0` with the object, or the object moved by a constant offset, in `rcx`; sizes 43 to 317 bytes |
| one-bit form | 331, which do not test bit `0x4`: 330 call `0x00809950`, and `0x00158DA0` calls `0x00210EB0`, which jumps on to `free` |
| two-bit form | 1,606, which test bit `0x4` after bit `0x1`: bit-clear side `0x00584730` (1,494), `0x007AD450` (93) and `0x0085E710` (19); bit-set side `0x0016D6A0` in all 1,606 |
| `PInputSource` family | 26 vtables at `0x01CD6268`–`0x01CD6588`; sizes `0x28` (20), `0x40` (4), `0x38` (2) |

The member lists beside this page, each named `object-construction-and-destruction-<list>.tsv`, list
compiler and library forms by function address; each was profiled against the image:

| List | Members |
|---|---|
| `counted-buffer-field-replace-98b`, `-99b` | 21 and 20 field replaces freeing the old buffer through `0x00584730` |
| `counted-buffer-list-materialisation` | 17 bodies that count a list, allocate (`0x0017D260`) and fill an array |
| `counted-buffer-release-and-clear` | 12 releases of a counted buffer |
| `refflag-dwordflag-alignedfree-reset-returntrue`, `refflag-invertedbit-alignedfree-returntrue` | 7 and 6 releases returning 1 |
| `refflag-handle-reset`, `refflag-handle-store-with-release` | 13 resets and 15 borrowed-pointer stores |
| `nativeadapter-refflag*` (five lists) | 4 or 5 each: releases and resizes of counted buffers inside larger records |
| `nativeadapter-dynamicoffsetrefflagbounded` | 4 resizes of a counted buffer found at a computed offset |
| `nativeadapter-countedalignedfreeloopself` | 4 frees of an array of records, each owning a buffer |
| `nativeleaf-refflag40strideaccessor`, `-72strideaccessor` | 4 and 4 element accessors with inline storage |
| `malloc-record-emplace-adapters` | 14 bodies that `malloc` a record and append it to a vector |
| `nativeadapter-lazysingletonallocinit` | 4 null-checked singletons allocated through `0x00210EC0` |
| `nativeadapter-multirecordvtableinit` | 4 constructors building EASTL containers with named allocators |
| `nativeadapter-containerpopfront`, `-countedemberloop`, `-boundedrangecopycompare` | 4 each: container pops, loops and keyed lookups |
| `nativeadapter-flaggedteardownchain` | 4 teardowns that close an event record only when its flag is set |
| `intrusive-virtual-node-dispose-loop`, `nativeleaf-listwalkvcallslot3` | 12 and 4 list clears through the allocator's slot `+0x18` |
| `nativeleaf-vectorbufferrelease`, `-vectordestroydeallocloop` | 5 and 5 vector releases, the second destroying each element first |
| `nativeleaf-bumpallocpop` | 2 cursor steps that copy `+0x10` to `+0x18` (`0x002714A0`) or `+0x20` (`0x002714E0`) and advance `+0x10` by `0x10` |
| `eastl-container-instances` | 76 vector, tree and list operations generated per element type, with the operation and element size of each |

## Modding notes

- Keep `edx` intact through a hook on a deleting destructor: bit `0x1` decides whether the storage is
  freed, and bit `0x4` whether it is kept.
- An object built by the game must be freed by the deallocator its destructor names. Memory from
  another heap passed to `0x00584730` or `0x00809950` corrupts the runtime heap.
- To find a class's size, read the `edx` value its destructor passes to the deallocator.
- A counted buffer whose bit `0x80000000` is set is not freed by the game; set it when a record should point at
  memory the game must not release.

## Related

- [Static initialisation and teardown](static-initialisation-and-teardown.md): the constructors and
  teardowns run around `main`.
- [Image hardening](image-hardening.md): the `ret 0` body at `0x0016D6A0`.
- [Lazy statics and one-time initialisation](lazy-statics-and-one-time-init.md): objects built on first
  use.
- [`memory-and-allocation.md`](memory-and-allocation.md) and [`msvc-containers.md`](msvc-containers.md): the allocators and containers behind these frees.
- [Class hierarchy](../Engine-Core/class-hierarchy.md) and
  [vtable methods](../Engine-Core/vtable-methods.md): every RTTI-named vtable and slot.
- [`object-construction-and-destruction-counted-buffer-field-replace-98b.tsv`](object-construction-and-destruction-counted-buffer-field-replace-98b.tsv):
  98-byte functions that replace a counted buffer field: they take the new size and buffer from a getter, allocate,
  free the record's old buffer through `0x00584730` when the record owns it, and store the size and pointer (21 rows).
- [`object-construction-and-destruction-counted-buffer-field-replace-99b.tsv`](object-construction-and-destruction-counted-buffer-field-replace-99b.tsv):
  the 99-byte form of the same replace, which tests the ownership flag in `edx` (20 rows).
- [`object-construction-and-destruction-counted-buffer-list-materialisation.tsv`](object-construction-and-destruction-counted-buffer-list-materialisation.tsv):
  222-byte functions that count the intrusive list at a global and, when the record's count differs, allocate that
  many pointers through `0x0017D260`, zero them, free the old buffer through `0x00584730`, store the count and pointer
  and copy the list in (17 rows).
- [`object-construction-and-destruction-counted-buffer-release-and-clear.tsv`](object-construction-and-destruction-counted-buffer-release-and-clear.tsv):
  68-byte functions that free a counted buffer through `0x00584730` when the record owns it and zero its size and
  pointer either way (12 rows).
- [`object-construction-and-destruction-intrusive-virtual-node-dispose-loop.tsv`](object-construction-and-destruction-intrusive-virtual-node-dispose-loop.tsv):
  functions that walk the circular intrusive list at `[rcx]` and dispose of each node through slot `+0x18` of the
  vtable at `[rdi+0x10]` until they are back at the head (12 rows).
- [`object-construction-and-destruction-malloc-record-emplace-adapters.tsv`](object-construction-and-destruction-malloc-record-emplace-adapters.tsv):
  functions that allocate a `0x18`-byte record with `malloc`, initialise it when the type needs it and push it into
  the caller's container (growth `0x001AB570`, member fetch `0x0018B4E0`), ending with a jump to `0x0018AFF0` (14 rows).
- [`object-construction-and-destruction-nativeadapter-boundedrangecopycompare.tsv`](object-construction-and-destruction-nativeadapter-boundedrangecopycompare.tsv):
  404-byte functions that copy and compare a bounded range into storage anchored at `[rcx+8]` through `0x0016D720`,
  `0x0016D840` and `0x001A3100`, checked with `memcmp` (`0x00861ED2`) (4 rows).
- [`object-construction-and-destruction-nativeadapter-containerpopfront.tsv`](object-construction-and-destruction-nativeadapter-containerpopfront.tsv):
  functions that, when the count at `+0x48` is not 0, take the head node from `+0x30`, lower the count, run
  `0x0016D6D0` and `0x0016DA60` on the node, call slot 3 of the object at `+0x50` with `0x28` and run `0x00199DB0` on
  `+0x58` (4 rows).
- [`object-construction-and-destruction-nativeadapter-countedalignedfreeloopself.tsv`](object-construction-and-destruction-nativeadapter-countedalignedfreeloopself.tsv):
  functions that free each owned pointer of the counted array of 16-byte elements at `[this+8]` through `0x00584730`,
  then free the object itself the same way (4 rows).
- [`object-construction-and-destruction-nativeadapter-countedemberloop.tsv`](object-construction-and-destruction-nativeadapter-countedemberloop.tsv):
  functions that, when `+0x90` is 0 and the count argument is not, call a member operation and then `0x00199DB0` on
  `+0x20` once per count, stepping the source by `0xA` (4 rows).
- [`object-construction-and-destruction-nativeadapter-dynamicoffsetrefflagbounded.tsv`](object-construction-and-destruction-nativeadapter-dynamicoffsetrefflagbounded.tsv):
  functions that compute an element pointer from the offsets at `+0x18` and `+0x48`, bound the index against its
  counted buffer's count and look the element up, returning `0xD` when the lookup fails (4 rows).
- [`object-construction-and-destruction-nativeadapter-flaggedteardownchain.tsv`](object-construction-and-destruction-nativeadapter-flaggedteardownchain.tsv):
  functions that close the lock record at `+0x90` through `0x005CD6D0` when the byte at `+0xB8` is set, tear down
  `+0x58` and `+0x20`, and end with a jump to a finishing function (4 rows).
- [`object-construction-and-destruction-nativeadapter-lazysingletonallocinit.tsv`](object-construction-and-destruction-nativeadapter-lazysingletonallocinit.tsv):
  functions that, while their global is null, allocate the object through `0x00210EC0`, initialise it and store it in
  the global (4 rows).
- [`object-construction-and-destruction-nativeadapter-multirecordvtableinit.tsv`](object-construction-and-destruction-nativeadapter-multirecordvtableinit.tsv):
  functions that zero three qwords of the output record, install vtables through `0x001EDF00` on `+0x18` and a stack
  record, zero `+0x20` and run `0x00199DB0`, `0x005CC8A0` and `0x005CD0A0` (4 rows).
- [`object-construction-and-destruction-nativeadapter-refflagalignedfreeclear.tsv`](object-construction-and-destruction-nativeadapter-refflagalignedfreeclear.tsv):
  functions that free the buffer through `0x00584730` when bit `0x80000000` of the count at `[this]` is clear, then
  zero the pointer and size (4 rows).
- [`object-construction-and-destruction-nativeadapter-refflagsiblingalignedfreeinit.tsv`](object-construction-and-destruction-nativeadapter-refflagsiblingalignedfreeinit.tsv):
  functions that run two member operations on the argument, free the buffer at `[rbx+0x40]` through `0x00584730` and
  clear its fields when the count's bit `0x80000000` and the count allow it, run a member operation and return 1 (5
  rows).
- [`object-construction-and-destruction-nativeadapter-refflagsiblingalignedfreereleasethis.tsv`](object-construction-and-destruction-nativeadapter-refflagsiblingalignedfreereleasethis.tsv):
  functions that free the buffer at `+0x10` through `0x00584730` when the count's bit `0x80000000` allows it and clear
  both fields (5 rows).
- [`object-construction-and-destruction-nativeadapter-refflagsiblingalignedfreetail.tsv`](object-construction-and-destruction-nativeadapter-refflagsiblingalignedfreetail.tsv):
  functions that run a member teardown and a second member operation, free the buffer at `[rbx+0x20]` through
  `0x00584730` when the count's bit `0x80000000` allows it, clear the fields and end with a jump to a finishing
  function (5 rows).
- [`object-construction-and-destruction-nativeadapter-refflagsiblingboundedlookup.tsv`](object-construction-and-destruction-nativeadapter-refflagsiblingboundedlookup.tsv):
  functions that bound the index against the count at `[this]` less bit `0x80000000`, pick the inline or the heap
  element and look it up; when the lookup fails they return `0xD` or free the range through `0x00584730` (4 rows).
- [`object-construction-and-destruction-nativeadapter-refflagsiblingboundedlookup2.tsv`](object-construction-and-destruction-nativeadapter-refflagsiblingboundedlookup2.tsv):
  a second form: the smaller of the index and that count, a lookup on `[this+8]`, `0xD` when it fails, and otherwise
  the range shrinks and its tail is freed through `0x00584730` (4 rows).
- [`object-construction-and-destruction-nativeleaf-bumpallocpop.tsv`](object-construction-and-destruction-nativeleaf-bumpallocpop.tsv):
  functions that store `[this+0x10]` to `+0x18` (`0x002714A0`) or `+0x20` (`0x002714E0`) and advance `+0x10` by `0x10`
  (2 rows).
- [`object-construction-and-destruction-nativeleaf-listwalkvcallslot3.tsv`](object-construction-and-destruction-nativeleaf-listwalkvcallslot3.tsv):
  functions that walk the intrusive list at `[this+0x18]`, calling a member operation with each node and then slot 3
  of the object at `+0x30` with `0x58` (4 rows).
- [`object-construction-and-destruction-nativeleaf-refflag40strideaccessor.tsv`](object-construction-and-destruction-nativeleaf-refflag40strideaccessor.tsv):
  accessors that return 0 for an index at or past the count at `+0x18` less bit `0x80000000`, and otherwise `+0x8`
  of the 40-byte element, inline at `+0x20` or on the heap (4 rows).
- [`object-construction-and-destruction-nativeleaf-refflag72strideaccessor.tsv`](object-construction-and-destruction-nativeleaf-refflag72strideaccessor.tsv):
  accessors that return `base + 0x20 + index * stride`: 40 bytes in `0x00623DB0` and `0x00623E30`, 72 bytes in
  `0x00670D80` and `0x00670DC0` (4 rows).
- [`object-construction-and-destruction-nativeleaf-vectorbufferrelease.tsv`](object-construction-and-destruction-nativeleaf-vectorbufferrelease.tsv):
  functions that compute a vector's count of 24-byte elements and release its buffer through slot `+0x18` of its
  allocator (5 rows).
- [`object-construction-and-destruction-nativeleaf-vectordestroydeallocloop.tsv`](object-construction-and-destruction-nativeleaf-vectordestroydeallocloop.tsv):
  functions that destroy each `0x18`-byte element of a vector through slot 0 of its vtable, then release the buffer
  through slot `+0x18` of the allocator with its size in bytes (5 rows).
- [`object-construction-and-destruction-refflag-dwordflag-alignedfree-reset-returntrue.tsv`](object-construction-and-destruction-refflag-dwordflag-alignedfree-reset-returntrue.tsv):
  functions that test a flag in the dword at `[rdx]`, free `[rdx+8]` through `0x00584730` when it is set, zero `+0x8`,
  `+0x0` and the flag dword, and return 1 (7 rows).
- [`object-construction-and-destruction-refflag-handle-reset.tsv`](object-construction-and-destruction-refflag-handle-reset.tsv):
  functions that, when the record owns its pointer, clear the ownership bit and release the pointer through a member
  function, then zero the size and pointer either way (13 rows).
- [`object-construction-and-destruction-refflag-handle-store-with-release.tsv`](object-construction-and-destruction-refflag-handle-store-with-release.tsv):
  functions that return 5 for a negative size; otherwise, when the stored pointer differs and the record owns it,
  they release it, store the size with bit `0x80000000` and the new pointer, and return 0 (15 rows).
- [`object-construction-and-destruction-refflag-invertedbit-alignedfree-returntrue.tsv`](object-construction-and-destruction-refflag-invertedbit-alignedfree-returntrue.tsv):
  functions that test a flag in the dword at `[rdx+0x30]`, free `[rdx+0x18]` through `0x00584730` when it is set, zero
  `+0x18` and `+0x30`, and return 1 (6 rows).

Each of these function tables has one row per function: `address` is where it starts and `targets` the functions it
calls or jumps to directly.
