---
title: "Animation channel binding: how an animation curve finds its target and how rotation, scale and translation become a bone matrix"
kind: "system"
category: "PhyreEngine"
addresses: "005C0820, 005C1160, 005C0C90, 005C0B60, 005C72A0, 005A7E90, 005C6020, 005C61A0, 01F2CE40, 01CEBBA8, 00D317D8, 00D31768, 005AF3B0, 005C0E00, 005C1000, 00D31850, 00D31868, 005B2D60"
---

## What the player sees

A PhyreEngine animation is a set of channels, each steering one property of one object. Rotation,
scale and translation channels of one target are combined into that target's matrix, and a target
whose animation has no scale channel keeps whatever scale it already had. In the shipped game this
path is used by two map models, where an animation switches one node's visibility; no character,
monster or weapon cluster carries a PhyreEngine animation.

## How it works

The work is split in two: binding, once per animation and target object, turns each channel target
into a target record; composition, every evaluation, writes channel values through those records.

### Channel semantics

A channel's meaning is a pointer to one of nineteen 24-byte descriptors in `.data` starting at
`01F2CE40` (stride `0x18`, ended by a null name at `01F2D008`). The composer compares the pointer
itself, so only these objects carry meaning.

| Descriptor | Name | Floats |
|---|---|---|
| `01F2CE40` | `Rotation` | 4 |
| `01F2CE58` | `Translation` | 3 |
| `01F2CE70` | `Scale` | 3 |
| `01F2CE88`–`01F2CED0` | `ShaderParameterF4`, `F3`, `F2`, `F1` | 4, 3, 2, 1 |
| `01F2CEE8`–`01F2CF18` | `LightColor`, `LightIntensity`, `LightFalloffAndPenumbra` | 4, 1, 2 |
| `01F2CF30`–`01F2CF78` | `CameraFov`, `CameraZNear`, `CameraZFar`, `CameraOrthographicSize` | 1 each |
| `01F2CF90` | `MorphTargetWeight` | 1 |
| `01F2CFA8`–`01F2CFF0` | `UserAttributeBool`, `Int`, `Float`, `Vector` | 1 each |

### Binders

`PAnimationChannelTargetBind` (`00D317D8`, slot 1 `_purecall`) has six subclasses, all created by `005B2D60`. Each slot-1 body
walks the binding descriptors (`0x38` apart) beside the target records (`0x30` apart), takes only
descriptors whose `+0x20` type matches its own, and only fills a record whose kind is still 0.

| Class | Slot 1 | Descriptor type | Record it writes |
|---|---|---|---|
| `PAnimationChannelTargetBindDataMember` | `005C0820` | 2 | kind 1: address and size |
| `PAnimationChannelTargetBindMethod` | `005C0C90` | 3 | kind 2: `+0x20` the method, `+0x18` the object |
| `PAnimationChannelTargetBindFunction` | `005C0B60` | 4 | kind 3: `+0x28` the function |
| `PAnimationChannelTargetBindShaderParameter` | `005C1160` | 5 | kind 1: address in the parameter buffer and size |
| `PAnimationChannelTargetBindScene` (`00D31850`) | `005C0E00` | 1 | kind 1: the node's `+0x20`, size `0x40` |
| `PAnimationChannelTargetBindSceneToMeshInstance` (`00D31868`) | `005C1000` | 1 | kind 1: a matrix-array entry, size `0x40` |

The data-member, method and function binders accept a descriptor only when its `+0x00` (the
instance class) is the class at the binder's `+0x08` or one reached from it through `+0x78`. The target
object is the binder's `+0x10`, else the descriptor's `+0x08`, and the binder's `+0x18` (when set) may
replace it through its vtable slot 2.

The method and function binders look the name up (`005A7B50`, `005A7AB0`) and log
`Bound method %s does not take a single const Vectormath::Aos::Vector4 * parameter...` (or `function`)
when the signature differs; they bind anyway.

### Resolving a data-member path

`005C0820` splits the name at each `.` (`strchr`) and looks each segment up with `00597220` in the
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

`005C1160` takes the parameter buffer from the binder's `+0x08`, or from the descriptor when its
`+0x00` is `02CB7480` (the descriptor's `+0x08` itself) or `02CB6B80` (that object's `+0x08`). It finds
the parameter by name with `0018D240`, takes the offset (`u16 +0x10`) and size (`u16 +0x12` & `0x1FFF`),
and binds only when the offset is at least 4 and offset + size fits the buffer's first dword.

### The scene binders

For descriptor type 1, `005B2D60` walks the objects it binds against. An object whose class is the
`PNode` descriptor `02E518D0` gets a `PAnimationChannelTargetBindScene`; one whose class chain reaches
the `PMeshInstance` descriptor `02CB6E80` gets a `PAnimationChannelTargetBindSceneToMeshInstance`.
Both accept a descriptor only when its instance class reaches `02E518D0` through `+0x78`, and fill
only a record whose kind is still 0.

- `005C0E00` collects the names and hands them to `005C35A0`, which hashes each name up to any `#`
  and finds the matching node under the binder's `+0x08`. A found node gives kind 1, the address
  node `+0x20` and size `0x40`.
- `005C1000` compares each name with the name table at `+0x48` (count `+0x30`) of the object at
  `[binder+0x08]+0x00`. A match at index `i` gives kind 1, the address `[binder+0x08]+0x18` + `i` ×
  `0x40` and size `0x40`.

### Composition

`005C72A0` (slot 12 of `PAnimationTargetBlenderController`, `00D31768`) walks the `0x18`-byte entries
at `[[this+0x10]+0x28]` (count `+0x20`). Entry `+0x10` is a channel index: it selects the 40-byte
value slot (four floats, semantic pointer at `+0x10`) and, through that entry's `+0x0C`, the target
record. Consecutive entries with the same target form a group; a kind-0 target skips its group.

1. A `Rotation` value is normalised (`s = 1 / sqrt(x² + y² + z² + w²)`) and sets bit `0x1`; `Scale` sets
   bit `0x2`; `Translation` sets bit `0x4`.
2. Any other non-null semantic is applied at once: kind 1 copies the four floats' first `size` bytes
   to the address, kind 2 calls `005A7E90(record+0x20, record+0x18, value)`, kind 3
   `005A7E90(record+0x28, 0, value)`.
3. At the end of a group with any bit set and a kind-1 target, it writes the matrix at the address.

`005A7E90(object, context, ...)` calls slot 2 of the object at `object+0x28` with the context, two
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

- weighted (`005C61A0`, `PAnimationWeightedBlenderController`): `mark[slot[i]] = 1` for every `i`
  whose weight is non-zero;
- additive (`005C6020`, `PAnimationAdditiveBlenderController`): `mark[slot[0]] = 1` whenever the
  count is non-zero, then the same rule from `i = 1`.

### Grouping channels by target

`005C22B0`, called from `005B1900`, collects the channels of a set of clips in a local ordered map
keyed by channel target. Two targets are the same key when their index (`+0x30`), type (`+0x20`),
the four object fields and the name match. The map's nodes are `0xA8` bytes from a `PMapPair` pool
(`0067FFB0`). Each node's value starts from a template at `01F2D010`; every channel ORs bit *n* (*n*
being its semantic's index, `+0x14`) into the value's first word and stores its `+0x40` in word
*n* + 1.

The function clears the map and a second local object (a buffer at `+0x08`, a tree at `+0x10`)
before it returns. When an exception leaves it, its unwind actions do the same: `005A9DF0` erases the
map's nodes (`0067FE20`) and frees the pool (`006803D0`, `00680030`), and `005AA080` resets the second
tree (`0067F6F0`), frees the buffer and clears the tree (`0067F580`).

### Network buffer planning

`005C62C0(network, freeFirst)` orders the `0x138`-byte nodes of an animation network and gives each
node output a buffer slot, reusing a slot once every reader of its value has run:

1. It marks every node unscheduled (`+0x130` = −1) and every output unassigned (state 0, slot −1).
2. It takes the first unscheduled node whose inputs all come from scheduled nodes and gives it the
   next order number. When no such node is left it returns 1.
3. Each output of the node gets a slot from the allocator (`005C0180`) and state 1.
4. Every output in state 1 that has a slot and whose readers have all been scheduled (`005C2F40`)
   gives its slot back and moves to state 2. With `freeFirst` set this step runs before step 3.

`005CA460` calls it with `freeFirst` 0 (`005CA5EE`), so a node's outputs are placed before the slots
freed by its own scheduling come back.

`005C2F40(node, output)` returns true when every node in the node's reader list (`+0x120` count,
`+0x128` data) that reads this output through one of its inputs has an order number. A reader that
does not read this output is ignored, and an output with no readers counts as read.

The allocator is a `PNetworkOptimizeBufferAllocator` on `005C62C0`'s stack: an array of 8-byte slots
(`u8` in use, `u32` size at `+0x04`) at `+0x08`, count `+0x10`. `005C0180(allocator, size,
acceptance)` returns the first of:

- the smallest free slot of non-zero size at least `size` that `acceptance` accepts;
- otherwise the largest accepted free slot of non-zero size;
- otherwise the first free slot of size 0;
- otherwise, after growing the array to twice its count or 16 more (`005C5A40`), a retry; −1 when
  that allocation fails.

It marks the slot in use and raises its size to `size`. The acceptance object is a
`PAvoidOutputOverwritingInput` (vtable `00D32B18`); its slot 0, `005C12D0`, rejects a slot that holds
one of the node's own inputs when that input's size is larger than the output's.

## Layouts

Binding descriptor (PAnimationChannelTarget, members registered by `005AF3B0`), `0x38` bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `void*` | m_instanceObjectType | class the target must be |
| `08` | `void*` | m_instanceObject | default target object |
| `10` | `void*` | m_baseObjectType |  |
| `18` | `void*` | m_baseObject |  |
| `20` | `u32` | m_type | 2 data member, 3 method, 4 function, 5 shader parameter |
| `28` | `void*` | m_name | path or name; bit 0 of the pointer is masked off |
| `30` | `u32` | m_index | array index |

Target record, `0x30` bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u32` | kind | 0 unbound, 1 address, 2 method, 3 function |
| `08` | `void*` | dest | kind 1 address, also the matrix base |
| `10` | `u32` | size | kind 1 bytes: at most `0x10`, or `0x40` from a scene binder |
| `18` | `void*` | context | kind 2 object |
| `20` | `void*` | method | kind 2 |
| `28` | `void*` | function | kind 3 |

Channel value slot, `0x28` bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `f32[4]` | value |  |
| `10` | `void*` | semantic | descriptor at `01F2CE40`..., null for none |

Channel semantic, `0x18` bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `void*` | name |  |
| `08` | `void*` | link | 0 in the image |
| `10` | `u32` | floats |  |
| `14` | `u32` | index | 0 in the image |

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
| `100` | `u32` | inputCount | bit 31 masked |
| `108` | `void*` | inputs | `0x10` bytes each: source node at +`0x00`, output index at +`0x08` |
| `110` | `u32` | outputCount | bit 31 masked |
| `118` | `void*` | outputs | `0x0C` bytes each: size, state (0, 1 placed, 2 released), slot |
| `120` | `u32` | readerCount | bit 31 masked |
| `128` | `void*` | readers | nodes that read this node's outputs |
| `130` | `i32` | order | -1 until scheduled |

## Shipped data

Measured over the packed namespaces and instance lists of every `.phyre` cluster in the archive.

| Fact | Value |
|---|---|
| clusters declaring any `PAnimation` class | 2: `map/bds01/bds0109/bds0109.dae.phyre`, `map/gil01/gil0102/gil0102.dae.phyre` |
| per cluster | 1 `PAnimationSet`, 1 `PAnimationClip`, 1 `PAnimationClipBinding`, 4 `PAnimationConstantChannel`, 4 `PAnimationSlotListIndex`, 2 `PAnimationChannelTarget` |
| channel targets | 4: in each cluster one with `m_type` 1 and one with `m_type` 3 |
| target names | `nodename1608` / `nodename118` (nodes, bound by the scene binders) and `setVisibilityFromAnimation` (a method, bound by `005C0C90`) |
| targets with `m_type` 2, 4 or 5 | 0 |

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
