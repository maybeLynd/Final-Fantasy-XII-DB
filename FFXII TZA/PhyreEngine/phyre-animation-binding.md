---
title: "Animation channel binding: how an animation curve finds its target and how rotation, scale and translation become a bone matrix"
kind: "system"
category: "PhyreEngine"
addresses: "0x005C0820, 0x005C1160, 0x005C0C90, 0x005C0B60, 0x005C72A0, 0x005A7E90, 0x005C6020, 0x005C61A0, 0x01F2CE40, 0x01CEBBA8, 0x00D317D8, 0x00D31768, 0x005AF3B0, 0x005C0E00, 0x005C1000, 0x00D31850, 0x00D31868, 0x005B2D60"
---

## What the player sees

A PhyreEngine animation is a set of channels, each steering one property of one object. Rotation,
scale and translation channels of one target are combined into that target's matrix, and a rotation
channel without a scale channel writes an unscaled rotation, so only a target animated by translation
alone keeps the rotation and scale it already had. In the shipped game this
path is used by two map models, where an animation switches one node's visibility; no character,
monster or weapon cluster carries a PhyreEngine animation.

## How it works

The work is split in two: binding, once per animation and target object, turns each channel target
into a target record; composition, every evaluation, writes channel values through those records.

### Channel semantics

A channel's meaning is a pointer to one of nineteen 24-byte descriptors in `.data` starting at
`0x01F2CE40` (stride `0x18`, ended by a null name at `0x01F2D008`). The composer compares the pointer
itself, so only these objects carry meaning.

| Descriptor | Name | Floats |
|---|---|---|
| `0x01F2CE40` | `Rotation` | 4 |
| `0x01F2CE58` | `Translation` | 3 |
| `0x01F2CE70` | `Scale` | 3 |
| `0x01F2CE88`–`0x01F2CED0` | `ShaderParameterF4`, `F3`, `F2`, `F1` | 4, 3, 2, 1 |
| `0x01F2CEE8`–`0x01F2CF18` | `LightColor`, `LightIntensity`, `LightFalloffAndPenumbra` | 4, 1, 2 |
| `0x01F2CF30`–`0x01F2CF78` | `CameraFov`, `CameraZNear`, `CameraZFar`, `CameraOrthographicSize` | 1 each |
| `0x01F2CF90` | `MorphTargetWeight` | 1 |
| `0x01F2CFA8`–`0x01F2CFF0` | `UserAttributeBool`, `Int`, `Float`, `Vector` | 1 each |

### Binders

`PAnimationChannelTargetBind` (`0x00D317D8`, slot 1 `_purecall`) has six subclasses, all created by `0x005B2D60`. Each slot-1 body
walks the binding descriptors (`0x38` apart) beside the target records (`0x30` apart), takes only
descriptors whose `+0x20` type matches its own, and only fills a record whose kind is still 0.

| Class | Slot 1 | Descriptor type | Record it writes |
|---|---|---|---|
| `PAnimationChannelTargetBindDataMember` | `0x005C0820` | 2 | kind 1: address and size |
| `PAnimationChannelTargetBindMethod` | `0x005C0C90` | 3 | kind 2: `+0x20` the method, `+0x18` the object |
| `PAnimationChannelTargetBindFunction` | `0x005C0B60` | 4 | kind 3: `+0x28` the function |
| `PAnimationChannelTargetBindShaderParameter` | `0x005C1160` | 5 | kind 1: address in the parameter buffer and size |
| `PAnimationChannelTargetBindScene` (`0x00D31850`) | `0x005C0E00` | 1 | kind 1: the node's `+0x20`, size `0x40` |
| `PAnimationChannelTargetBindSceneToMeshInstance` (`0x00D31868`) | `0x005C1000` | 1 | kind 1: a matrix-array entry, size `0x40` |

The data-member, method and function binders accept a descriptor only when its `+0x00` (the
instance class) is the class at the binder's `+0x08` or one reached from it through `+0x78`. The target
object is the binder's `+0x10`, else the descriptor's `+0x08`, and the binder's `+0x18` (when set) may
replace it through its vtable slot 2.

The method and function binders look the name up (`0x005A7B50`, `0x005A7AB0`) and log
`Bound method %s does not take a single const Vectormath::Aos::Vector4 * parameter...` (or `function`)
when the signature differs; they bind anyway.

### Resolving a data-member path

`0x005C0820` splits the name at each `.` (`strchr`) and looks each segment up with `0x00597220` in the
current class, adding the member's offset (`member+0x48` minus `[member+0x18]+0xF4`) as it descends.
A segment with no matching member leaves the record unbound without a log line. For the final member, the as-array
accessor (member vtable slot 1) gives the array kind at `+0x5C`:

- 0 (a scalar): the size is the type's element size (`[member+0x30]+0x38`), or 8 when member flag
  bit 1 (`+0x28`) marks a pointer member;
- 1 to 4 (the array kinds): the index (descriptor `+0x30`) must be below the count (array slot 4),
  else it logs `Not binding %s:%s because array index (%d) exceeds array size (%d)` and skips; the
  address is the array base (slot 6) plus index × element size;
- above 4: the record is left unbound.

The record gets kind 1, the address at `+0x08` and the size at `+0x10`, clamped to 16 bytes.

### The shader-parameter binder

`0x005C1160` takes the parameter buffer from the binder's `+0x08`, or from the descriptor when its
`+0x00` is `0x02CB7480` (the descriptor's `+0x08` itself) or `0x02CB6B80` (that object's `+0x08`). It finds
the parameter by name with `0x0018D240`, takes the offset (`u16 +0x10`) and size (`u16 +0x12` & `0x1FFF`),
and binds only when the offset is at least 4 and offset + size fits the buffer's first dword.

### The scene binders

For descriptor type 1, `0x005B2D60` walks the objects it binds against. An object whose class is the
`PNode` descriptor `0x02E518D0` gets a `PAnimationChannelTargetBindScene`; one whose class chain reaches
the `PMeshInstance` descriptor `0x02CB6E80` gets a `PAnimationChannelTargetBindSceneToMeshInstance`.
Both accept a descriptor only when its instance class reaches `0x02E518D0` through `+0x78`, and fill
only a record whose kind is still 0.

- `0x005C0E00` collects the names and hands them to `0x005C35A0`, which hashes each name up to any `#`
  and finds the matching node under the binder's `+0x08`. A found node gives kind 1, the address
  node `+0x20` and size `0x40`.
- `0x005C1000` compares each name with the name table at `+0x48` (count `+0x30`) of the object at
  `[binder+0x08]+0x00`. A match at index `i` gives kind 1, the address `[binder+0x08]+0x18` + `i` ×
  `0x40` and size `0x40`.

### Composition

`0x005C72A0` (slot 12 of `PAnimationTargetBlenderController`, `0x00D31768`) walks the `0x18`-byte entries
at `[[this+0x10]+0x28]` (count `+0x20`). Entry `+0x10` is a channel index: it selects the 40-byte
value slot (four floats, semantic pointer at `+0x10`) and, through that entry's `+0x0C`, the target
record. Consecutive entries with the same target form a group; a kind-0 target skips its group.

1. A `Rotation` value is normalised (`s = 1 / sqrt(x² + y² + z² + w²)`) and sets bit `0x1`; `Scale` sets
   bit `0x2`; `Translation` sets bit `0x4`.
2. Any other non-null semantic is applied at once: kind 1 copies the four floats' first `size` bytes
   to the address, kind 2 calls `0x005A7E90(record+0x20, record+0x18, value)`, kind 3
   `0x005A7E90(record+0x28, 0, value)`.
3. At the end of a group with any bit set and a kind-1 target, it writes the matrix at the address.

`0x005A7E90(object, context, ...)` calls slot 2 of the object at `object+0x28` with the context, two
zeros, and a pointer to its own variadic argument area holding the value pointer.

### Matrix arithmetic

With `(X, Y, Z, W)` the normalised quaternion, `S` the scale and `T` the translation, writing floats of
the 4×4 matrix by index (row-major rows of the basis):

| Bits | Floats 0–2 | Floats 4–6 | Floats 8–10 |
|---|---|---|---|
| rotation | `1−2Y²−2Z²`, `2XY+2ZW`, `2XZ−2YW` | `2XY−2ZW`, `1−2X²−2Z²`, `2YZ+2WX` | `2XZ+2YW`, `2YZ−2WX`, `1−2X²−2Y²` |
| scale | `Sx`, 0, 0 | 0, `Sy`, 0 | 0, 0, `Sz` |
| both | the rotation row × `Sx` | the rotation row × `Sy` | the rotation row × `Sz` |

Translation writes floats 12–14 = `Tx`, `Ty`, `Tz`. Floats 3, 7, 11 and 15 are never written, and a
group without rotation or scale leaves 0–10 as they were.

### Slot marking in the blenders

Slot 9 of the two blender controllers marks which output slots contribute, from the weights at
controller `+0x30`:

- weighted (`0x005C61A0`, `PAnimationWeightedBlenderController`): `mark[slot[i]] = 1` for every `i`
  whose weight is non-zero;
- additive (`0x005C6020`, `PAnimationAdditiveBlenderController`): `mark[slot[0]] = 1` whenever the
  count is non-zero, then the same rule from `i = 1`.

### Grouping channels by target

`0x005C22B0`, called from `0x005B1900`, collects the channels of a set of clips in a local ordered map
keyed by channel target. Two targets are the same key when their index (`+0x30`), type (`+0x20`),
the four object fields and the name match. The map's nodes are `0xA8` bytes from a `PMapPair` pool
(`0x0067FFB0`). Each node's value starts from a template at `0x01F2D010`; every channel ORs bit *n* (*n*
being its semantic's index, `+0x14`) into the value's first word and stores its `+0x40` in word
*n* + 1.

The function clears the map and a second local object (a buffer at `+0x08`, a tree at `+0x10`)
before it returns. When an exception leaves it, its unwind actions do the same: `0x005A9DF0` erases the
map's nodes (`0x0067FE20`) and frees the pool (`0x006803D0`, `0x00680030`), and `0x005AA080` resets the second
tree (`0x0067F6F0`), frees the buffer and clears the tree (`0x0067F580`).

### Network buffer planning

`0x005C62C0(network, freeFirst)` orders the `0x138`-byte nodes of an animation network and gives each
node output a buffer slot, reusing a slot once every reader of its value has run:

1. It marks every node unscheduled (`+0x130` = −1) and every output unassigned (state 0, slot −1).
2. It takes the first unscheduled node whose inputs all come from scheduled nodes and gives it the
   next order number. When no such node is left it returns 1.
3. Each output of the node gets a slot from the allocator (`0x005C0180`) and state 1.
4. Every output in state 1 that has a slot and whose readers have all been scheduled (`0x005C2F40`)
   gives its slot back and moves to state 2. With `freeFirst` set this step runs before step 3.

`0x005CA460` calls it with `freeFirst` 0 (`0x005CA5EE`), so a node's outputs are placed before the slots
freed by its own scheduling come back.

`0x005C2F40(node, output)` returns true when every node in the node's reader list (`+0x120` count,
`+0x128` data) that reads this output through one of its inputs has an order number. A reader that
does not read this output is ignored, and an output with no readers counts as read.

The allocator is a `PNetworkOptimizeBufferAllocator` on `0x005C62C0`'s stack: an array of 8-byte slots
(`u8` in use, `u32` size at `+0x04`) at `+0x08`, count `+0x10`. `0x005C0180(allocator, size,
acceptance)` returns the first of:

- the smallest free slot of non-zero size at least `size` that `acceptance` accepts;
- otherwise the largest accepted free slot of non-zero size;
- otherwise the first free slot of size 0;
- otherwise, after growing the array to twice its count or 16 more (`0x005C5A40`), a retry; −1 when
  that allocation fails.

It marks the slot in use and raises its size to `size`. The acceptance object is a
`PAvoidOutputOverwritingInput` (vtable `0x00D32B18`); its slot 0, `0x005C12D0`, rejects a slot that holds
one of the node's own inputs when that input's size is larger than the output's.

## Layouts

### Reflected members

The members below are the ones the code of this page's classes uses or the reflection registers; each registered member is named by its registration (the registering function, through 0x00632960), and each class fence covers only those members.

`PAnimationChannel` (`0x68` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x60` | `u32` | m_keyCount | m_keyCount (u32), registered by `0x005AF0A0` (`0x00632960` at `0x005AF242`); the cluster loader binds it by name (`0x0059B430`) in the 2 shipped .phyre files that declare PAnimationChannel; the placement constructor `0x005A26F0` sets it to 0 (`0x005A2742`) |
| `+0x64` | `u8[4]` | pad64 | the bytes after m_keyCount (+`0x60`) up to the end of the `0x68`-byte class; no registered member covers it (`0x005A80B0` registers the `0x68`-byte class at `0x005A80FA`) |

`PAnimationChannelTarget` (`0x38` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x28` | `void*` | m_name | path or name; bit 0 of the pointer is masked off; m_name (ptr), registered by `0x005AF3B0` (`0x00632960` at `0x005AF9AB`); the cluster loader binds it by name (`0x0059B430`) in the 2 shipped .phyre files that declare PAnimationChannelTarget; the script method getTargetName (registered at `0x005AF5C9`) returns it through `0x005C5320`, which clears bit 0; the placement constructor `0x005A0F60` clears it (`0x005A0F99`) |
| `+0x30` | `u32` | m_index | array index; m_index (u32), registered by `0x005AF3B0` (`0x00632960` at `0x005AFA1E`); the cluster loader binds it by name (`0x0059B430`) in the 2 shipped .phyre files that declare PAnimationChannelTarget; the script method getTargetIndex (registered at `0x005AF693`) returns it through `0x0079CFA0`; the placement constructor `0x005A0F60` clears it (`0x005A0F9D`) |
| `+0x34` | `u8[4]` | pad34 | the bytes after m_index (+`0x30`) up to the end of the `0x38`-byte class; no registered member covers it (`0x005A81F0` registers the `0x38`-byte class at `0x005A8240`) |

`PAnimationChannelTimes` (`0x18` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | m_keyCount | m_keyCount (u32), registered by `0x005AFA60` (`0x00632960` at `0x005AFB8C`); the cluster loader binds it by name (`0x0059B430`) in the 2 shipped .phyre files that declare PAnimationChannelTimes; the placement constructor `0x005A5090` sets it to 0 (`0x005A5097`) |
| `+0x04` | `u8[4]` | pad04 | alignment bytes between m_keyCount (u32 at +`0x00`) and m_timeKeys (PArray at +`0x08`); no registered member covers it (`0x005A82A0` registers the `0x18`-byte class at `0x005A82F0`) |

`PAnimationClip` (`0x38` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x30` | `void*` | m_name | m_name (ptr), registered by `0x005AFBC0` (`0x00632960` at `0x005B06BC`); the cluster loader binds it by name (`0x0059B430`) in the 2 shipped .phyre files that declare PAnimationClip; the script method getName (registered at `0x005AFD14`) returns its address through `0x005C4D20`; the placement constructor `0x005A1BA0` clears it (`0x005A1BB8`) |

`PAnimationClipBinding` (`0x8` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | m_spuBindingSize | m_spuBindingSize (u16), registered by `0x005B0700` (`0x00632960` at `0x005B0795`); the cluster loader binds it by name (`0x0059B430`) in the 2 shipped .phyre files that declare PAnimationClipBinding |
| `+0x02` | `u16` | m_channelCount | m_channelCount (u16), registered by `0x005B0700` (`0x00632960` at `0x005B0808`); the cluster loader binds it by name (`0x0059B430`) in the 2 shipped .phyre files that declare PAnimationClipBinding |
| `+0x04` | `u16` | m_constantChannelCount m_constantChannelCount (u16), registered by 0x005B0700 (0x00632960 at | `0x005B087B`); the cluster loader binds it by name (`0x0059B430`) in the 2 shipped .phyre files that declare PAnimationClipBinding |
| `+0x06` | `u16` | m_interpCountLength | m_interpCountLength (u16), registered by `0x005B0700` (`0x00632960` at `0x005B08EE`); the cluster loader binds it by name (`0x0059B430`) in the 2 shipped .phyre files that declare PAnimationClipBinding |

`PAnimationClipBindingDataBlockCache` (`0x18` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x10` | `u32` | m_valueWidthAndKeyCount m_valueWidthAndKeyCount (u32), registered by 0x005B0A70 (0x00632960 at | `0x005B0B7C`); the cluster loader binds it by name (`0x0059B430`) in the 2 shipped .phyre files that declare PAnimationClipBindingDataBlockCache; the placement constructor `0x005A4C40` clears +`0x10` to +`0x17` with one qword store (`0x005A4C4E`) |
| `+0x14` | `u16` | m_sourceChannelIndex | m_sourceChannelIndex (u16), registered by `0x005B0A70` (`0x00632960` at `0x005B0B09`); the cluster loader binds it by name (`0x0059B430`) in the 2 shipped .phyre files that declare PAnimationClipBindingDataBlockCache; cleared with m_valueWidthAndKeyCount by the placement constructor `0x005A4C40` (`0x005A4C4E`) |
| `+0x16` | `u8[2]` | pad16 | the bytes after m_sourceChannelIndex (u16 at +`0x14`) up to the end of the `0x18`-byte class; cleared with it by the placement constructor `0x005A4C40` (`0x005A4C4E`); no registered member covers it (`0x005A8560` registers the `0x18`-byte class at `0x005A85B0`) |

`PAnimationNetworkInstance` (`0x78` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x0C` | `u8[4]` | pad0C | the four bytes between the array count at +`0x08` and its pointer at +`0x10`, both released by the destructor `0x005A9F10` (`0x005A9FA7`, `0x005A9FB3`); no registered member covers it (`0x005A8B50` registers the `0x78`-byte class at `0x005A8BA0`) |
| `+0x1C` | `u8[4]` | pad1C | the four bytes between the array count at +`0x18` and its pointer at +`0x20`, both released by the destructor `0x005A9F10` (`0x005A9F85`, `0x005A9F91`); no registered member covers it (`0x005A8B50` registers the `0x78`-byte class at `0x005A8BA0`) |
| `+0x38` | `u32` | m_slotArrayElementsRequired m_slotArrayElementsRequired (u32), registered by 0x005B14E0 | (`0x00632960` at `0x005B1716`); no shipped .phyre file declares PAnimationNetworkInstance |
| `+0x3C` | `u8[4]` | bytes3C | the four bytes after m_slotArrayElementsRequired (+`0x38`), before the array count at +`0x40`; no registered member covers it (`0x005A8B50` registers the `0x78`-byte class at `0x005A8BA0`) |
| `+0x44` | `u8[4]` | pad44 | the four bytes between the array count at +`0x40` and its pointer at +`0x48`, both released by the destructor `0x005A9F10` (`0x005A9F63`, `0x005A9F6F`); no registered member covers it (`0x005A8B50` registers the `0x78`-byte class at `0x005A8BA0`) |
| `+0x50` | `u32` | m_preprocessBufferSize m_preprocessBufferSize (u32), registered by 0x005B14E0 (0x00632960 at | `0x005B1827`); no shipped .phyre file declares PAnimationNetworkInstance |
| `+0x54` | `u8[4]` | bytes54 | the four bytes after m_preprocessBufferSize (+`0x50`), before the array count at +`0x58`; no registered member covers it (`0x005A8B50` registers the `0x78`-byte class at `0x005A8BA0`) |
| `+0x5C` | `u8[4]` | pad5C | the four bytes between the array count at +`0x58` and its pointer at +`0x60`, both released by the destructor `0x005A9F10` (`0x005A9F41`, `0x005A9F4D`); no registered member covers it (`0x005A8B50` registers the `0x78`-byte class at `0x005A8BA0`) |

`PAnimationSlotListIndex` (`0x18` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x0C` | `u32` | m_targetIndex | m_targetIndex (u32), registered by `0x005B20D0` (`0x00632960` at `0x005B2243`); the cluster loader binds it by name (`0x0059B430`) in the 2 shipped .phyre files that declare PAnimationSlotListIndex; the placement constructor `0x005A3CB0` sets it to 0 with the qword store that sets m_interp (+`0x08`) to 3 (`0x005A3CB7`) |
| `+0x10` | `u32` | m_nodeCentricReIndex | m_nodeCentricReIndex (u32), registered by `0x005B20D0` (`0x00632960` at `0x005B22B6`); the cluster loader binds it by name (`0x0059B430`) in the 2 shipped .phyre files that declare PAnimationSlotListIndex; the placement constructor `0x005A3CB0` sets it to 0 (`0x005A3CC2`) |
| `+0x14` | `u8[4]` | pad14 | the bytes after m_nodeCentricReIndex (+`0x10`) up to the end of the `0x18`-byte class; no registered member covers it (`0x005A8F60` registers the `0x18`-byte class at `0x005A8FB0`) |

`PNode` (`0x68` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x60` | `void*` | m_name | the node's name; m_name (ptr), registered by `0x006B41A0` (`0x00632960` at `0x006B5005`); the cluster loader binds it by name (`0x0059B430`) in the 2,097 shipped .phyre files that declare PNode; the script methods getName (registered at `0x006B48C8`) and setName (`0x006B47F3`) reach it through `0x00837860`, which returns its address, and `0x006B6050` |

`PAnimationSlotFilter` (`0x40` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x1C` | `u8[4]` | pad1C | the four bytes between the array count at +`0x18` and its pointer at +`0x20`, both released by the destructor `0x005AA0E0` (`0x005AA126`, `0x005AA132`); no registered member covers it (`0x005A8E10` registers the `0x40`-byte class at `0x005A8E5A`) |

`PAnimationAdditiveBlenderController` (`0x38` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x2C` | `u8[4]` | pad2C | the four bytes between the array count at +`0x28` and its pointer at +`0x30`, both released by the destructor `0x005A9CF0` (`0x005A9D11`, `0x005A9D1D`); no registered member covers it (`0x005A7F70` registers the `0x38`-byte class at `0x005A7FBA`) |

`PAnimationBlenderController` (`0x28` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x1C` | `u8[4]` | pad1C | the four bytes between the array count at +`0x18` and its pointer at +`0x20`, both released by the destructor `0x005AC9B0` (`0x005AC9D3`, `0x005AC9DF`); no registered member covers it (`0x005A8010` registers the `0x28`-byte class at `0x005A805A`) |

`PAnimationHierarchyNode` (`0x10` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x08` | `u8[8]` | bytes08 | the eight bytes after the vtable pointer (`0x00D312F0` for the base class); no registered member covers it (`0x005A8AA0` registers the `0x10`-byte class at `0x005A8AF0`) |

`PAnimationWeightedBlenderController` (`0x38` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x2C` | `u8[4]` | pad2C | the four bytes between the array count at +`0x28` and its pointer at +`0x30`, both released by the destructor `0x005AA1D0` (`0x005AA1F1`, `0x005AA1FD`); no registered member covers it (`0x005A9150` registers the `0x38`-byte class at `0x005A919A`) |

### Binding records

The structures below are the ones the mechanisms above use.

Binding descriptor (PAnimationChannelTarget, members registered by `0x005AF3B0`), `0x38` bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | m_instanceObjectType | class the target must be |
| `+0x08` | `void*` | m_instanceObject | default target object |
| `+0x10` | `void*` | m_baseObjectType |  |
| `+0x18` | `void*` | m_baseObject |  |
| `+0x20` | `u32` | m_type | 2 data member, 3 method, 4 function, 5 shader parameter |
| `+0x28` | `void*` | m_name | path or name; bit 0 of the pointer is masked off |
| `+0x30` | `u32` | m_index | array index |

Target record, `0x30` bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | kind | 0 unbound, 1 address, 2 method, 3 function |
| `+0x08` | `void*` | dest | kind 1 address, also the matrix base |
| `+0x10` | `u32` | size | kind 1 bytes: at most `0x10`, or `0x40` from a scene binder |
| `+0x18` | `void*` | context | kind 2 object |
| `+0x20` | `void*` | method | kind 2 |
| `+0x28` | `void*` | function | kind 3 |

Channel value slot, `0x28` bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `f32[4]` | value |  |
| `+0x10` | `void*` | semantic | descriptor at `0x01F2CE40`..., null for none |

Channel semantic, `0x18` bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | name |  |
| `+0x08` | `void*` | link | 0 in the image |
| `+0x10` | `u32` | floats |  |
| `+0x14` | `u32` | index | 0 in the image |

Instruction-level access tables per class, beside this page:

| Class | Table |
|---|---|
| `PAnimationChannel` | [phyre-animation-binding-panimation-channel-accesses.tsv](phyre-animation-binding-panimation-channel-accesses.tsv) |
| `PAnimationChannelBase` | [phyre-animation-binding-panimation-channel-base-accesses.tsv](phyre-animation-binding-panimation-channel-base-accesses.tsv) |
| `PAnimationChannelTarget` | [phyre-animation-binding-panimation-channel-target-accesses.tsv](phyre-animation-binding-panimation-channel-target-accesses.tsv) |
| `PAnimationChannelTimes` | [phyre-animation-binding-panimation-channel-times-accesses.tsv](phyre-animation-binding-panimation-channel-times-accesses.tsv) |
| `PAnimationClip` | [phyre-animation-binding-panimation-clip-accesses.tsv](phyre-animation-binding-panimation-clip-accesses.tsv) |
| `PAnimationClipBindingDataBlockCache` | [phyre-animation-binding-panimation-clip-binding-data-block-cache-accesses.tsv](phyre-animation-binding-panimation-clip-binding-data-block-cache-accesses.tsv) |
| `PAnimationNetworkInstanceTarget` | [phyre-animation-binding-panimation-network-instance-target-accesses.tsv](phyre-animation-binding-panimation-network-instance-target-accesses.tsv) |
| `PAnimationSlotArray` | [phyre-animation-binding-panimation-slot-array-accesses.tsv](phyre-animation-binding-panimation-slot-array-accesses.tsv) |
| `PAnimationSlotListIndex` | [phyre-animation-binding-panimation-slot-list-index-accesses.tsv](phyre-animation-binding-panimation-slot-list-index-accesses.tsv) |
| `PAnimatableComponent` | [phyre-animation-binding-panimatable-component-accesses.tsv](phyre-animation-binding-panimatable-component-accesses.tsv) |
| `PAnimationAdditiveBlenderController` | [phyre-animation-binding-panimation-additive-blender-controller-accesses.tsv](phyre-animation-binding-panimation-additive-blender-controller-accesses.tsv) |
| `PAnimationBlenderController` | [phyre-animation-binding-panimation-blender-controller-accesses.tsv](phyre-animation-binding-panimation-blender-controller-accesses.tsv) |
| `PAnimationHierarchyNode` | [phyre-animation-binding-panimation-hierarchy-node-accesses.tsv](phyre-animation-binding-panimation-hierarchy-node-accesses.tsv) |
| `PAnimationNetworkInstance` | [phyre-animation-binding-panimation-network-instance-accesses.tsv](phyre-animation-binding-panimation-network-instance-accesses.tsv) |
| `PAnimationSlotFilter` | [phyre-animation-binding-panimation-slot-filter-accesses.tsv](phyre-animation-binding-panimation-slot-filter-accesses.tsv) |
| `PAnimationWeightedBlenderController` | [phyre-animation-binding-panimation-weighted-blender-controller-accesses.tsv](phyre-animation-binding-panimation-weighted-blender-controller-accesses.tsv) |

`PAnimationNetworkNode` (`0x138` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x100` | `u32` | inputCount | bit 31 masked |
| `+0x108` | `void*` | inputs | `0x10` bytes each: source node at +`0x00`, output index at +`0x08` |
| `+0x110` | `u32` | outputCount | bit 31 masked |
| `+0x118` | `void*` | outputs | `0x0C` bytes each: size, state (0, 1 placed, 2 released), slot |
| `+0x120` | `u32` | readerCount | bit 31 masked |
| `+0x128` | `void*` | readers | nodes that read this node's outputs |
| `+0x130` | `i32` | order | -1 until scheduled |

## Shipped data

Measured over the packed namespaces and instance lists of every `.phyre` cluster in the archive.

| Fact | Value |
|---|---|
| clusters declaring any `PAnimation` class | 2: `map/bds01/bds0109/bds0109.dae.phyre`, `map/gil01/gil0102/gil0102.dae.phyre` |
| per cluster | 1 `PAnimationSet`, 1 `PAnimationClip`, 1 `PAnimationClipBinding`, 4 `PAnimationConstantChannel`, 4 `PAnimationSlotListIndex`, 2 `PAnimationChannelTarget` |
| channel targets | 4: in each cluster one with `m_type` 1 and one with `m_type` 3 |
| target names | `nodename1608` / `nodename118` (nodes, bound by the scene binders) and `setVisibilityFromAnimation` (a method, bound by `0x005C0C90`) |
| targets with `m_type` 2, 4 or 5 | 0 |

## State

### Semantic indices

Each channel semantic is built by its own static initialiser, which runs before `main` in initialiser-table order
(`0x008C35C8`-`0x008C3658`). The initialiser reads the count `0x02CACF18`, stores it in the descriptor's `+0x14`, stores
the count plus 1 back, puts the descriptor's address in the table `0x02CACF20` at the old count, and registers an
exit teardown. After the nineteenth the count is 19 and each semantic's index is its row number in Channel semantics.

A semantic's index is the bit it owns in a channel group's word. `0x005C22B0` reads `+0x14` through a channel's
semantic pointer (`+0x38`) and ORs `1 << index` into the group (`0x005C26FA`-`0x005C26FC`); `0x005C2FE0` and `0x005C8130`
read it the same way and combine `index << 2` with the channel's `+0x40` (`0x005C307A`, `0x005C8237`). `0x005CB8D0` walks
the bits of a group word up to the count and takes each set bit's semantic from `0x02CACF20` (`0x005CBB95`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x01F2CE54` | `u32` | 0 | `Rotation` (`0x01F2CE40`) `+0x14`: index 0 | `0x00160DF0` (`0x00160E01`, 0) | `0x005C22B0` (`0x005C26EF`, `0x005C29BF`), `0x005C2FE0` (`0x005C3077`), `0x005C8130` (`0x005C8234`, `0x005C82E4`), through a channel's semantic pointer `+0x38` |
| `0x01F2CE6C` | `u32` | 0 | `Translation` (`0x01F2CE58`) `+0x14`: index 1 | `0x00160F70` (`0x00160F81`, 1) | `0x005C22B0` (`0x005C26EF`, `0x005C29BF`), `0x005C2FE0` (`0x005C3077`), `0x005C8130` (`0x005C8234`, `0x005C82E4`), through a channel's semantic pointer `+0x38` |
| `0x01F2CE84` | `u32` | 0 | `Scale` (`0x01F2CE70`) `+0x14`: index 2 | `0x00160E30` (`0x00160E41`, 2) | `0x005C22B0` (`0x005C26EF`, `0x005C29BF`), `0x005C2FE0` (`0x005C3077`), `0x005C8130` (`0x005C8234`, `0x005C82E4`), through a channel's semantic pointer `+0x38` |
| `0x01F2CE9C` | `u32` | 0 | `ShaderParameterF4` (`0x01F2CE88`) `+0x14`: index 3 | `0x00160F30` (`0x00160F41`, 3) | `0x005C22B0` (`0x005C26EF`, `0x005C29BF`), `0x005C2FE0` (`0x005C3077`), `0x005C8130` (`0x005C8234`, `0x005C82E4`), through a channel's semantic pointer `+0x38` |
| `0x01F2CEB4` | `u32` | 0 | `ShaderParameterF3` (`0x01F2CEA0`) `+0x14`: index 4 | `0x00160EF0` (`0x00160F01`, 4) | `0x005C22B0` (`0x005C26EF`, `0x005C29BF`), `0x005C2FE0` (`0x005C3077`), `0x005C8130` (`0x005C8234`, `0x005C82E4`), through a channel's semantic pointer `+0x38` |
| `0x01F2CECC` | `u32` | 0 | `ShaderParameterF2` (`0x01F2CEB8`) `+0x14`: index 5 | `0x00160EB0` (`0x00160EC1`, 5) | `0x005C22B0` (`0x005C26EF`, `0x005C29BF`), `0x005C2FE0` (`0x005C3077`), `0x005C8130` (`0x005C8234`, `0x005C82E4`), through a channel's semantic pointer `+0x38` |
| `0x01F2CEE4` | `u32` | 0 | `ShaderParameterF1` (`0x01F2CED0`) `+0x14`: index 6 | `0x00160E70` (`0x00160E81`, 6) | `0x005C22B0` (`0x005C26EF`, `0x005C29BF`), `0x005C2FE0` (`0x005C3077`), `0x005C8130` (`0x005C8234`, `0x005C82E4`), through a channel's semantic pointer `+0x38` |
| `0x01F2CEFC` | `u32` | 0 | `LightColor` (`0x01F2CEE8`) `+0x14`: index 7 | `0x00160CF0` (`0x00160D01`, 7) | `0x005C22B0` (`0x005C26EF`, `0x005C29BF`), `0x005C2FE0` (`0x005C3077`), `0x005C8130` (`0x005C8234`, `0x005C82E4`), through a channel's semantic pointer `+0x38` |
| `0x01F2CF14` | `u32` | 0 | `LightIntensity` (`0x01F2CF00`) `+0x14`: index 8 | `0x00160D70` (`0x00160D81`, 8) | `0x005C22B0` (`0x005C26EF`, `0x005C29BF`), `0x005C2FE0` (`0x005C3077`), `0x005C8130` (`0x005C8234`, `0x005C82E4`), through a channel's semantic pointer `+0x38` |
| `0x01F2CF2C` | `u32` | 0 | `LightFalloffAndPenumbra` (`0x01F2CF18`) `+0x14`: index 9 | `0x00160D30` (`0x00160D41`, 9) | `0x005C22B0` (`0x005C26EF`, `0x005C29BF`), `0x005C2FE0` (`0x005C3077`), `0x005C8130` (`0x005C8234`, `0x005C82E4`), through a channel's semantic pointer `+0x38` |
| `0x01F2CF44` | `u32` | 0 | `CameraFov` (`0x01F2CF30`) `+0x14`: index 10 | `0x00160BF0` (`0x00160C01`, 10) | `0x005C22B0` (`0x005C26EF`, `0x005C29BF`), `0x005C2FE0` (`0x005C3077`), `0x005C8130` (`0x005C8234`, `0x005C82E4`), through a channel's semantic pointer `+0x38` |
| `0x01F2CF5C` | `u32` | 0 | `CameraZNear` (`0x01F2CF48`) `+0x14`: index 11 | `0x00160CB0` (`0x00160CC1`, 11) | `0x005C22B0` (`0x005C26EF`, `0x005C29BF`), `0x005C2FE0` (`0x005C3077`), `0x005C8130` (`0x005C8234`, `0x005C82E4`), through a channel's semantic pointer `+0x38` |
| `0x01F2CF74` | `u32` | 0 | `CameraZFar` (`0x01F2CF60`) `+0x14`: index 12 | `0x00160C70` (`0x00160C81`, 12) | `0x005C22B0` (`0x005C26EF`, `0x005C29BF`), `0x005C2FE0` (`0x005C3077`), `0x005C8130` (`0x005C8234`, `0x005C82E4`), through a channel's semantic pointer `+0x38` |
| `0x01F2CF8C` | `u32` | 0 | `CameraOrthographicSize` (`0x01F2CF78`) `+0x14`: index 13 | `0x00160C30` (`0x00160C41`, 13) | `0x005C22B0` (`0x005C26EF`, `0x005C29BF`), `0x005C2FE0` (`0x005C3077`), `0x005C8130` (`0x005C8234`, `0x005C82E4`), through a channel's semantic pointer `+0x38` |
| `0x01F2CFA4` | `u32` | 0 | `MorphTargetWeight` (`0x01F2CF90`) `+0x14`: index 14 | `0x00160DB0` (`0x00160DC1`, 14) | `0x005C22B0` (`0x005C26EF`, `0x005C29BF`), `0x005C2FE0` (`0x005C3077`), `0x005C8130` (`0x005C8234`, `0x005C82E4`), through a channel's semantic pointer `+0x38` |
| `0x01F2CFBC` | `u32` | 0 | `UserAttributeBool` (`0x01F2CFA8`) `+0x14`: index 15 | `0x00160FB0` (`0x00160FC1`, 15) | `0x005C22B0` (`0x005C26EF`, `0x005C29BF`), `0x005C2FE0` (`0x005C3077`), `0x005C8130` (`0x005C8234`, `0x005C82E4`), through a channel's semantic pointer `+0x38` |
| `0x01F2CFD4` | `u32` | 0 | `UserAttributeInt` (`0x01F2CFC0`) `+0x14`: index 16 | `0x00161030` (`0x00161041`, 16) | `0x005C22B0` (`0x005C26EF`, `0x005C29BF`), `0x005C2FE0` (`0x005C3077`), `0x005C8130` (`0x005C8234`, `0x005C82E4`), through a channel's semantic pointer `+0x38` |
| `0x01F2CFEC` | `u32` | 0 | `UserAttributeFloat` (`0x01F2CFD8`) `+0x14`: index 17 | `0x00160FF0` (`0x00161001`, 17) | `0x005C22B0` (`0x005C26EF`, `0x005C29BF`), `0x005C2FE0` (`0x005C3077`), `0x005C8130` (`0x005C8234`, `0x005C82E4`), through a channel's semantic pointer `+0x38` |
| `0x01F2D004` | `u32` | 0 | `UserAttributeVector` (`0x01F2CFF0`) `+0x14`: index 18 | `0x00161070` (`0x00161081`, 18) | `0x005C22B0` (`0x005C26EF`, `0x005C29BF`), `0x005C2FE0` (`0x005C3077`), `0x005C8130` (`0x005C8234`, `0x005C82E4`), through a channel's semantic pointer `+0x38` |
| `0x02CACF18` | `u32` | 0 (zero-filled tail of .data) | number of channel semantics registered, the next free row of `0x02CACF20`; 19 after the nineteen initialisers | the nineteen initialisers, each the count plus 1: `0x00160BF0` (`0x00160C07`), `0x00160C30` (`0x00160C47`), `0x00160C70` (`0x00160C87`), `0x00160CB0` (`0x00160CC7`), `0x00160CF0` (`0x00160D07`), `0x00160D30` (`0x00160D47`), `0x00160D70` (`0x00160D87`), `0x00160DB0` (`0x00160DC7`), `0x00160DF0` (`0x00160E07`), `0x00160E30` (`0x00160E47`), `0x00160E70` (`0x00160E87`), `0x00160EB0` (`0x00160EC7`), `0x00160EF0` (`0x00160F07`), `0x00160F30` (`0x00160F47`), `0x00160F70` (`0x00160F87`), `0x00160FB0` (`0x00160FC7`), `0x00160FF0` (`0x00161007`), `0x00161030` (`0x00161047`), `0x00161070` (`0x00161087`) | the same nineteen initialisers, each at its first instruction, and `0x005C2FE0` (`0x005C3001`) and `0x005C8130` (`0x005C81C4`), which size a stack buffer from it, `0x005C8850` (`0x005C8864`), which passes it to `0x0060C340`, and `0x005CB8D0` (`0x005CBB70`, `0x005CBBB5`), which stops its walk at it |

### The semantic registry

The `PAnimation` init `0x005C5C80` also puts the semantics on a registry keyed by name, `0x02CAFCD8`, linked through
each descriptor's `+0x08`. It inserts `Rotation`, `Translation`, `Scale` and `ShaderParameterF4` itself
(`0x005C5D6F`-`0x005C5EF9`) and the other fifteen through `0x005BEFE0` (15 calls).

Each insert walks the list comparing
names and returns `0x12` for a name already present (`0x11` for a null name in `0x005BEFE0`); otherwise it stores the
old head in the descriptor's `+0x08` and makes the descriptor the head.

The `PAnimation` shutdown `0x005CB150` takes
them off again, the first six inline and the rest through `0x005BFED0`: its walk pointer starts at the head, so its
store `[r9]` writes the head or the `+0x08` of the descriptor before, and it then stores 0 in the descriptor's own
`+0x08`.

The other readers are `0x005BF070`, which stores the descriptor whose name matches through its first argument
or returns `0x13`, `0x005C38B0`, which copies every descriptor's address into an array it allocates with `0x0017D260`,
and `0x005C5250`, which returns the descriptor whose name matches, or 0.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02CAFCD8` | `void*` | 0 (zero-filled tail of `.data`) | head of the semantic registry | `0x005C5C80` (`0x005C5DD9`, `0x005C5E39`, `0x005C5E99`, `0x005C5EF9`); `0x005BEFE0` (`0x005BF04A`); through the unlink pointer, `0x005CB150` (`0x005CB228`, `0x005CB278`, `0x005CB2C8`, `0x005CB318`, `0x005CB368`, `0x005CB3B8`) and `0x005BFED0` | `0x005BEFE0` (`0x005BEFFC`); `0x005BF070` (`0x005BF082`); `0x005BFED0` (`0x005BFED0`); `0x005C38B0` (`0x005C38BF`, `0x005C3950`); `0x005C5250` (`0x005C525B`); `0x005C5C80` (`0x005C5D7B`); `0x005CB150` (`0x005CB1E8`, `0x005CB22F`, `0x005CB27F`, `0x005CB2CF`, `0x005CB31F`, `0x005CB36F`, `0x005CB3BF`) |
| `0x01F2CE48` | `void*` | 0 (file-backed `.data`) | `Rotation` (`0x01F2CE40`) `+0x08`: the head before it, 0 | `0x005C5C80` (`0x005C5DCB`); `0x005CB150` (`0x005CB22B`, 0, through the descriptor) | every walk of the list, through the descriptor; `0x005CB150` compares its address (`0x005CB1F7`) |
| `0x01F2CE60` | `void*` | 0 (file-backed `.data`) | `Translation` (`0x01F2CE58`) `+0x08`: `Rotation` | `0x005C5C80` (`0x005C5E2B`); `0x005CB150` (`0x005CB27B`, 0, through the descriptor) | every walk of the list, through the descriptor; `0x005CB150` compares its address (`0x005CB241`) |
| `0x01F2CE78` | `void*` | 0 (file-backed `.data`) | `Scale` (`0x01F2CE70`) `+0x08`: `Translation` | `0x005C5C80` (`0x005C5E8B`); `0x005CB150` (`0x005CB2CB`, 0, through the descriptor) | every walk of the list, through the descriptor; `0x005CB150` compares its address (`0x005CB291`) |
| `0x01F2CE90` | `void*` | 0 (file-backed `.data`) | `ShaderParameterF4` (`0x01F2CE88`) `+0x08`: `Scale` | `0x005C5C80` (`0x005C5EEB`); `0x005CB150` (`0x005CB31B`, 0, through the descriptor) | every walk of the list, through the descriptor; `0x005CB150` compares its address (`0x005CB2E1`) |

The walks that read a descriptor's `+0x08` are in `0x005BEFE0`, `0x005BF070`, `0x005BFED0`, `0x005C38B0`, `0x005C5250`,
`0x005C5C80` and `0x005CB150`. The unlink stores through `[r9]` also write one of these four links when the descriptor
removed is the one after it.

## Modding notes

- A channel's semantic must point at the shipped descriptor; a copy with the same name is treated as a
  non-transform channel.
- The matrix's floats 3, 7, 11 and 15 must already hold `0, 0, 0, 1`.
- A non-transform channel on a data-member or shader-parameter target never receives more than
  16 bytes. A group with a rotation, scale or translation channel writes the matrix floats 0–2,
  4–6, 8–10 and 12–14 (up to byte 60) at the record's address, whatever its size; a scene target's
  size is `0x40`.
- A misspelt data-member path binds nothing and logs nothing; an out-of-range array index is logged.
- Setting a target record's kind to 0 disables that channel's group.

## Related

- [Phyre reflection](phyre-reflection.md): class descriptors, member records and array kinds the binder walks.
- [Phyre field schema](phyre-field-schema.md): file-side against runtime member layouts.
- [Phyre asset files](phyre-asset-files.md): the clusters that carry animation sets.
- [Vtable methods](../Engine-Core/vtable-methods.md): the vtable slot convention used here.
