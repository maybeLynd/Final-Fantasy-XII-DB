---
title: "Object construction and destruction: vtable installs, deleting destructors, deallocators and owned buffers"
kind: "system"
category: "Compiler and C runtime"
addresses: "00809950, 00210EB0, 0019C590, 00584730, 0019C570, 0016D6A0, 007AD450, 0085E710, 00210EC0, 001D70A0, 00195530, 0086CE50, 01CD6268, 0015BC40, 00792350, 001EDF00, 005CA130, 00627750, 00623F50, 0019CA20, 001A4250"
---

## What the player sees

Nothing directly. Every character, effect, sound object and menu element is built and freed through
these few patterns, and a hook that breaks one of them shows up as a crash or a slow leak when objects
are created or destroyed, typically on area changes.

## How it works

### Constructors install vtables base first

A constructor stores a vtable with `lea reg, [vtable]; mov [object], reg`. A derived constructor calls
its base constructor, which stores the base vtable, and then overwrites it with its own. The C++ table
entry `0015BC40` shows both steps for the game's application object `01F7E350`: the base constructor
`00792350` stores `Phyre::PFramework::PApplication`'s vtable `01CB2508`, and `0015BC40` then stores
`GameApplication`'s vtable `008C5760` (`0015BC61`).

Every vtable is preceded by a pointer to its RTTI complete-object locator, so `vtable[-1]` names the
class; see [class hierarchy](../Engine-Core/class-hierarchy.md).

### The scalar deleting destructor

Slot 0 of a class with a virtual destructor is its scalar deleting destructor. It takes the object in
`rcx` and a flag in `edx`, destroys the object, frees it when bit `0x1` is set, and returns the object
in `rax`. The size it passes to the deallocator is the class size. The flag is tested where it arrives
or, when the destructor calls another function first, in the register it was saved to:

- `001D70A0` stores `ExtraUI`'s vtable, tests `dl, 1` (`001D70B3`) and calls `00809950` with
  `edx = 0x90`.
- `00195530` copies `edx` to `ebx` (`0019553A`), calls the inner destructor `00195180`, then tests
  `bl, 1` (`00195544`) and calls `00809950` with `edx = 0x98`.

`00809950` jumps to `00210EB0`, which jumps to `0019C590`, the `free` import stub; the size is ignored.

### The two-bit form

Most destructors test a second bit. `0086CE50` is the whole pattern:

1. Store the vtable, then test bit `0x1` (`0086CE6C`); when clear, return the object.
2. Test bit `0x4` (`0086CE71`).
3. Clear: call `00584730`, which is `if (p) _aligned_free(p)` (`0019C570` is the `_aligned_free` import
   stub).
4. Set: load the size (`edx = 0x28`) and call `0016D6A0`, which is `ret 0`.

A caller passing `0x5` therefore destroys the object and keeps its storage. Two other deallocators sit
on the bit-clear side: `007AD450` frees the block whose base is stored 8 bytes before the object,
through the function pointer at `02EAD0B8`, and `0085E710` counts the free in `02EAF6C8` and jumps
through the pointer at `01F44CF8`.

### Destructors rewind to the base vtable

The 26 vtables at `01CD6268`, one every `0x20` bytes, are `Phyre::PInputs::PInputSource` and its 25
subclasses; each one's own RTTI locator names it. Every slot-0 destructor stores the base vtable
`01CD6268` into the object before testing the flags, and then passes its own class's size to the
sized-delete call. A destructor's vtable store therefore names the class whose destructor runs next,
not the class it belongs to; the class comes from where the destructor's address sits.

| Vtable | Class | Destructor | Size |
|---|---|---|---|
| `01CD6268` | `PInputSource` | `0086CE50` | `0x28` |
| `01CD6288` | `PInputSourceKey` | `0086CF40` | `0x40` |
| `01CD62A8` | `PInputSourceJoypadButton` | `0086CEF0` | `0x40` |
| `01CD62C8` | `PInputSourceJoypadAxis` | `0086CEA0` | `0x38` |
| `01CD62E8` | `PInputSourceMouseButton` | `0086D2B0` | `0x38` |
| `01CD6308` | `PInputSourceMouseDeltaX` | `0086D300` | `0x40` |
| `01CD6328` | `PInputSourceMouseDeltaY` | `0086D350` | `0x40` |
| `01CD6348` | `PInputSourceTouchRotate` | `0086D490` | `0x28` |
| `01CD6368` | `PInputSourceTouchPinch` | `0086D440` | `0x28` |
| `01CD6388` | `PInputSourceTouchTwoFingerDragX` | `0086D4E0` | `0x28` |
| `01CD63A8` | `PInputSourceTouchTwoFingerDragY` | `0086D530` | `0x28` |
| `01CD63C8` | `PInputSourceTouchDragX` | `0086D3A0` | `0x28` |
| `01CD63E8` | `PInputSourceTouchDragY` | `0086D3F0` | `0x28` |
| `01CD6408` | `PInputSourceMotionQuatX` | `0086D1C0` | `0x28` |
| `01CD6428` | `PInputSourceMotionQuatY` | `0086D210` | `0x28` |
| `01CD6448` | `PInputSourceMotionQuatZ` | `0086D260` | `0x28` |
| `01CD6468` | `PInputSourceMotionQuatW` | `0086D170` | `0x28` |
| `01CD6488` | `PInputSourceMotionAngularVelocityX` | `0086CF90` | `0x28` |
| `01CD64A8` | `PInputSourceMotionAngularVelocityY` | `0086CFE0` | `0x28` |
| `01CD64C8` | `PInputSourceMotionAngularVelocityZ` | `0086D030` | `0x28` |
| `01CD64E8` | `PInputSourceMotionLinearAccelerationX` | `0086D080` | `0x28` |
| `01CD6508` | `PInputSourceMotionLinearAccelerationY` | `0086D0D0` | `0x28` |
| `01CD6528` | `PInputSourceMotionLinearAccelerationZ` | `0086D120` | `0x28` |
| `01CD6548` | `PInputSourceVisionTrackerX` | `0086D580` | `0x28` |
| `01CD6568` | `PInputSourceVisionTrackerY` | `0086D5D0` | `0x28` |
| `01CD6588` | `PInputSourceVisionTrackerZ` | `0086D620` | `0x28` |

Slot 2 of the base is `_purecall` (`00861EC6`) and every subclass fills it. Slot 1 of the base and of
the 19 touch, motion and vision-tracker classes is `0016D6A0`; the key, joypad and mouse classes fill it.

### Counted buffers with an ownership bit

Many records hold an array as two fields: a 32-bit count whose bit 31 marks storage the record
does not own, and a pointer. The release helpers free the pointer through `00584730` only when bit 31
is clear and then zero both fields (`005DD620`, `00597B00`). A replace frees the old pointer under the
same test before storing the new one (`00672990`). `005CA130` stores a borrowed pointer and sets bit 31
with the count.

In some records a count of 0 or 1 keeps the element inline in the pointer field: `00627750` and the
accessor `00623F50` use the field itself as the element when `count & 0x7FFFFFFF` is below 2, and
dereference it otherwise. A tagged-pointer variant marks borrowed storage with bit 0 of the pointer
instead (`005A17A0`).

### Allocator-owned containers

EASTL containers carry an allocator object whose vtable slot `+0x18` frees `(pointer, bytes)`.
`001EDF00` installs the `eastl::allocator_memory_log` vtable; containers pass it a name such as
`EASTL vector` or `EASTL set` (`0019C630`). A vector release calls the allocator with its buffer and
capacity in bytes (`0019CA20`); list clears walk the nodes and release each through the same slot
(`00199B00`).

The compiler generates the container operations once per element type. 76 such bodies between
`00188640` and `001FFF00` are listed in `object-construction-and-destruction-eastl-container-instances.tsv`
with the operation and element size of each: vector reserve, insert, erase, copy, fill and release,
tree copy, erase and node creation, list insert and clear, and element copy constructors.

Two examples: `001AF000` inserts `n` copies into a vector of `0x40`-byte elements, growing the buffer to
the larger of twice the old count (1 when empty) and the new count, and `001BA990` erases a range of
`0x2A8`-byte `ChrModel` elements, destroying each through slot 0 of its vtable.

Five of them are destructors of one class template that pairs these containers with a lock:
`00199A80`, `0019C870`, `0019DAD0`, `001B3AF0` and `001E74F0`. Each destroys the PhyreEngine lock
record at `+0x90` (`0x28` bytes; see [runtime services](runtime-services.md)) through `005CD6D0`,
which closes the event at lock `+0x08`, when the byte at `+0xB8` is set. It then erases the trees at
`+0x58` and `+0x20` (`0x28`-byte nodes; `001E7560` for `001E74F0`) and frees the vector at `+0x00`,
whose elements are `0x10`, `0x18`, `0x118`, `0x20` and `0x10` bytes.

The template is the record pool that [game application](../Engine-Core/game-application.md)
describes: its constructor `001997F0` builds the lock at `+0x90` with `005CC8A0` and stores the
flag at `+0xB8`, and `00199A80` is the destructor that the unwind funclet `00896C60` of
`001999D0` runs on the `AsyncJobManager` pool at `+0x90`.

`001E74F0` is reached only from the unwind funclet `008985BE` of `001E71B0`. `001E76B0`, from the
unwind funclet `00898660` of `001E7480`, releases a vector of `0x3C`-byte elements: it divides the
byte span by 60 and multiplies by `0x3C`.

`00210EC0` is a one-argument allocation entry: it sets `r8d = -1` and `edx = 0` and
jumps to the `malloc` import stub `0085E730`; the lazy singleton `0018A620` allocates its object through it.

## Layouts

```
scalar deleting destructor, as the call sites see it
  rcx = object
  edx = flags   0x1  free the storage
                0x4  sized delete (0016D6A0, frees nothing) instead of 00584730
  rax = object on return

counted buffer, 16 bytes
  +0x00  u32   count     bits 0..30 element count, bit 31 storage not owned
  +0x08  u64   data      pointer; the element itself when the count is below 2 (inline form)

PInputSource vtable, 0x20 bytes per class from 01CD6260
  -0x08  u64   locator   RTTI complete-object locator
  +0x00  u64   slot0     scalar deleting destructor
  +0x08  u64   slot1
  +0x10  u64   slot2
```

## Shipped data

| Fact | Value |
|---|---|
| deleting destructors | about 2,000 bodies under 400 bytes that test bit `0x1` of the incoming flag and then call a deallocator (1,985 to 2,008 depending on how chained entries and register moves are followed) |
| one-bit form | about 400, most through `00809950`, the rest through `00584730` |
| two-bit form | about 1,600; bit-clear side mostly `00584730`, then `007AD450` and `0085E710`; bit-set side `0016D6A0` in all |
| `PInputSource` family | 26 vtables at `01CD6268`–`01CD6588`; sizes `0x28` (20), `0x40` (4), `0x38` (2) |

The member lists beside this page, each named `object-construction-and-destruction-<list>.tsv`, list
compiler and library forms by function address; each was profiled against the image:

| List | Members |
|---|---|
| `counted-buffer-field-replace-98b`, `-99b` | 21 and 20 field replaces freeing the old buffer through `00584730` |
| `counted-buffer-list-materialisation` | 17 bodies that count a list, allocate (`0017D260`) and fill an array |
| `counted-buffer-release-and-clear` | 12 releases of a counted buffer |
| `refflag-dwordflag-alignedfree-reset-returntrue`, `refflag-invertedbit-alignedfree-returntrue` | 7 and 6 releases returning 1 |
| `refflag-handle-reset`, `refflag-handle-store-with-release` | 13 resets and 15 borrowed-pointer stores |
| `nativeadapter-refflag*` (five lists) | 4 or 5 each: releases and resizes of counted buffers inside larger records |
| `nativeadapter-dynamicoffsetrefflagbounded` | 4 resizes of a counted buffer found at a computed offset |
| `nativeadapter-countedalignedfreeloopself` | 4 frees of an array of records, each owning a buffer |
| `nativeleaf-refflag40strideaccessor`, `-72strideaccessor` | 4 and 4 element accessors with inline storage |
| `malloc-record-emplace-adapters` | 14 bodies that `malloc` a record and append it to a vector |
| `nativeadapter-lazysingletonallocinit` | 4 null-checked singletons allocated through `00210EC0` |
| `nativeadapter-multirecordvtableinit` | 4 constructors building EASTL containers with named allocators |
| `nativeadapter-containerpopfront`, `-countedemberloop`, `-boundedrangecopycompare` | 4 each: container pops, loops and keyed lookups |
| `nativeadapter-flaggedteardownchain` | 4 teardowns that close an event record only when its flag is set |
| `intrusive-virtual-node-dispose-loop`, `nativeleaf-listwalkvcallslot3` | 12 and 4 list clears through the allocator's slot `+0x18` |
| `nativeleaf-vectorbufferrelease`, `-vectordestroydeallocloop` | 5 and 5 vector releases, the second destroying each element first |
| `nativeleaf-bumpallocpop` | 2 cursor steps that copy `+0x10` to `+0x18` and advance `+0x10` by `0x10` |
| `eastl-container-instances` | 76 vector, tree and list operations generated per element type, with the operation and element size of each |

## Modding notes

- Keep `edx` intact through a hook on a deleting destructor: bit `0x1` decides whether the storage is
  freed, and bit `0x4` whether it is kept.
- An object built by the game must be freed by the deallocator its destructor names. Memory from
  another heap passed to `00584730` or `00809950` corrupts the runtime heap.
- To find a class's size, read the `edx` value its destructor passes to the deallocator.
- A counted buffer whose bit 31 is set is not freed by the game; set it when a record should point at
  memory the game must not release.

## Related

- [Static initialisation and teardown](static-initialisation-and-teardown.md): the constructors and
  teardowns run around `main`.
- [Image hardening](image-hardening.md): the `ret 0` body at `0016D6A0`.
- [Lazy statics and one-time initialisation](lazy-statics-and-one-time-init.md): objects built on first
  use.
- `memory-and-allocation.md` and `msvc-containers.md`: the allocators and containers behind these frees.
- [Class hierarchy](../Engine-Core/class-hierarchy.md) and
  [vtable methods](../Engine-Core/vtable-methods.md): every RTTI-named vtable and slot.
