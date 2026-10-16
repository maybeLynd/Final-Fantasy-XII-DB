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
`01F2CE40` (stride `18`<sub>h</sub>, ended by a null name at `01F2D008`). The composer compares the pointer
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
walks the binding descriptors (`38`<sub>h</sub> apart) beside the target records (`30`<sub>h</sub> apart), takes only
descriptors whose `+20`<sub>h</sub> type matches its own, and only fills a record whose kind is still 0.

| Class | Slot 1 | Descriptor type | Record it writes |
|---|---|---|---|
| `PAnimationChannelTargetBindDataMember` | `005C0820` | 2 | kind 1: address and size |
| `PAnimationChannelTargetBindMethod` | `005C0C90` | 3 | kind 2: `+20`<sub>h</sub> the method, `+18`<sub>h</sub> the object |
| `PAnimationChannelTargetBindFunction` | `005C0B60` | 4 | kind 3: `+28`<sub>h</sub> the function |
| `PAnimationChannelTargetBindShaderParameter` | `005C1160` | 5 | kind 1: address in the parameter buffer and size |
| `PAnimationChannelTargetBindScene` (`00D31850`) | `005C0E00` | 1 | kind 1: the node's `+20`<sub>h</sub>, size `40`<sub>h</sub> |
| `PAnimationChannelTargetBindSceneToMeshInstance` (`00D31868`) | `005C1000` | 1 | kind 1: a matrix-array entry, size `40`<sub>h</sub> |

The data-member, method and function binders accept a descriptor only when its `+00`<sub>h</sub> (the
instance class) is the class at the binder's `+08`<sub>h</sub> or one reached from it through `+78`<sub>h</sub>. The target
object is the binder's `+10`<sub>h</sub>, else the descriptor's `+08`<sub>h</sub>, and the binder's `+18`<sub>h</sub> (when set) may
replace it through its vtable slot 2.

The method and function binders look the name up (`005A7B50`, `005A7AB0`) and log
`Bound method %s does not take a single const Vectormath::Aos::Vector4 * parameter...` (or `function`)
when the signature differs; they bind anyway.

### Resolving a data-member path

`005C0820` splits the name at each `.` (`strchr`) and looks each segment up with `00597220` in the
current class, adding the member's offset (`member+48h` minus `[member+18h]+F4h`) as it descends.
A segment with no matching member leaves the record unbound without a log line. For the final member, the as-array
accessor (member vtable slot 1) gives the array kind at `+5C`<sub>h</sub>:

- 0 (a scalar): the size is the type's element size (`[member+30h]+38h`), or 8 when member flag
  bit 1 (`+28`<sub>h</sub>) marks a pointer member;
- 1 to 4 (the array kinds): the index (descriptor `+30`<sub>h</sub>) must be below the count (array slot 4),
  else it logs `Not binding %s:%s because array index (%d) exceeds array size (%d)` and skips; the
  address is the array base (slot 6) plus index × element size;
- above 4: the record is left unbound.

The record gets kind 1, the address at `+08`<sub>h</sub> and the size at `+10`<sub>h</sub>, clamped to 16 bytes.

### The shader-parameter binder

`005C1160` takes the parameter buffer from the binder's `+08`<sub>h</sub>, or from the descriptor when its
`+00`<sub>h</sub> is `02CB7480` (the descriptor's `+08`<sub>h</sub> itself) or `02CB6B80` (that object's `+08`<sub>h</sub>). It finds
the parameter by name with `0018D240`, takes the offset (`u16 +10h`) and size (`u16 +12h` & `1FFF`<sub>h</sub>),
and binds only when the offset is at least 4 and offset + size fits the buffer's first dword.

### The scene binders

For descriptor type 1, `005B2D60` walks the objects it binds against. An object whose class is the
`PNode` descriptor `02E518D0` gets a `PAnimationChannelTargetBindScene`; one whose class chain reaches
the `PMeshInstance` descriptor `02CB6E80` gets a `PAnimationChannelTargetBindSceneToMeshInstance`.
Both accept a descriptor only when its instance class reaches `02E518D0` through `+78`<sub>h</sub>, and fill
only a record whose kind is still 0.

- `005C0E00` collects the names and hands them to `005C35A0`, which hashes each name up to any `#`
  and finds the matching node under the binder's `+08`<sub>h</sub>. A found node gives kind 1, the address
  node `+20`<sub>h</sub> and size `40`<sub>h</sub>.
- `005C1000` compares each name with the name table at `+48`<sub>h</sub> (count `+30`<sub>h</sub>) of the object at
  `[binder+08h]+00h`. A match at index `i` gives kind 1, the address `[binder+08h]+18h` + `i` ×
  `40`<sub>h</sub> and size `40`<sub>h</sub>.

### Composition

`005C72A0` (slot 12 of `PAnimationTargetBlenderController`, `00D31768`) walks the `18`<sub>h</sub>-byte entries
at `[[this+10h]+28h]` (count `+20`<sub>h</sub>). Entry `+10`<sub>h</sub> is a channel index: it selects the 40-byte
value slot (four floats, semantic pointer at `+10`<sub>h</sub>) and, through that entry's `+0C`<sub>h</sub>, the target
record. Consecutive entries with the same target form a group; a kind-0 target skips its group.

1. A `Rotation` value is normalised (`s = 1 / sqrt(x² + y² + z² + w²)`) and sets bit `1`<sub>h</sub>; `Scale` sets
   bit `2`<sub>h</sub>; `Translation` sets bit `4`<sub>h</sub>.
2. Any other non-null semantic is applied at once: kind 1 copies the four floats' first `size` bytes
   to the address, kind 2 calls `005A7E90(record+20h, record+18h, value)`, kind 3
   `005A7E90(record+28h, 0, value)`.
3. At the end of a group with any bit set and a kind-1 target, it writes the matrix at the address.

`005A7E90(object, context, ...)` calls slot 2 of the object at `object+28h` with the context, two
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
controller `+30`<sub>h</sub>:

- weighted (`005C61A0`, `PAnimationWeightedBlenderController`): `mark[slot[i]] = 1` for every `i`
  whose weight is non-zero;
- additive (`005C6020`, `PAnimationAdditiveBlenderController`): `mark[slot[0]] = 1` whenever the
  count is non-zero, then the same rule from `i = 1`.

### Grouping channels by target

`005C22B0`, called from `005B1900`, collects the channels of a set of clips in a local ordered map
keyed by channel target. Two targets are the same key when their index (`+30`<sub>h</sub>), type (`+20`<sub>h</sub>),
the four object fields and the name match. The map's nodes are `A8`<sub>h</sub> bytes from a `PMapPair` pool
(`0067FFB0`). Each node's value starts from a template at `01F2D010`; every channel ORs bit *n* (*n*
being its semantic's index, `+14`<sub>h</sub>) into the value's first word and stores its `+40`<sub>h</sub> in word
*n* + 1.

The function clears the map and a second local object (a buffer at `+08`<sub>h</sub>, a tree at `+10`<sub>h</sub>)
before it returns. When an exception leaves it, its unwind actions do the same: `005A9DF0` erases the
map's nodes (`0067FE20`) and frees the pool (`006803D0`, `00680030`), and `005AA080` resets the second
tree (`0067F6F0`), frees the buffer and clears the tree (`0067F580`).

### Network buffer planning

`005C62C0(network, freeFirst)` orders the `138`<sub>h</sub>-byte nodes of an animation network and gives each
node output a buffer slot, reusing a slot once every reader of its value has run:

1. It marks every node unscheduled (`+130`<sub>h</sub> = −1) and every output unassigned (state 0, slot −1).
2. It takes the first unscheduled node whose inputs all come from scheduled nodes and gives it the
   next order number. When no such node is left it returns 1.
3. Each output of the node gets a slot from the allocator (`005C0180`) and state 1.
4. Every output in state 1 that has a slot and whose readers have all been scheduled (`005C2F40`)
   gives its slot back and moves to state 2. With `freeFirst` set this step runs before step 3.

`005CA460` calls it with `freeFirst` 0 (`005CA5EE`), so a node's outputs are placed before the slots
freed by its own scheduling come back.

`005C2F40(node, output)` returns true when every node in the node's reader list (`+120`<sub>h</sub> count,
`+128`<sub>h</sub> data) that reads this output through one of its inputs has an order number. A reader that
does not read this output is ignored, and an output with no readers counts as read.

The allocator is a `PNetworkOptimizeBufferAllocator` on `005C62C0`'s stack: an array of 8-byte slots
(`u8` in use, `u32` size at `+04`<sub>h</sub>) at `+08`<sub>h</sub>, count `+10`<sub>h</sub>. `005C0180(allocator, size,
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

Binding descriptor (PAnimationChannelTarget, members registered by `005AF3B0`), `38`<sub>h</sub> bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `void*` | m_instanceObjectType | class the target must be |
| `08`<sub>h</sub> | `void*` | m_instanceObject | default target object |
| `10`<sub>h</sub> | `void*` | m_baseObjectType |  |
| `18`<sub>h</sub> | `void*` | m_baseObject |  |
| `20`<sub>h</sub> | `u32` | m_type | 2 data member, 3 method, 4 function, 5 shader parameter |
| `28`<sub>h</sub> | `void*` | m_name | path or name; bit 0 of the pointer is masked off |
| `30`<sub>h</sub> | `u32` | m_index | array index |

Target record, `30`<sub>h</sub> bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u32` | kind | 0 unbound, 1 address, 2 method, 3 function |
| `08`<sub>h</sub> | `void*` | dest | kind 1 address, also the matrix base |
| `10`<sub>h</sub> | `u32` | size | kind 1 bytes: at most `10`<sub>h</sub>, or `40`<sub>h</sub> from a scene binder |
| `18`<sub>h</sub> | `void*` | context | kind 2 object |
| `20`<sub>h</sub> | `void*` | method | kind 2 |
| `28`<sub>h</sub> | `void*` | function | kind 3 |

Channel value slot, `28`<sub>h</sub> bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `f32[4]` | value |  |
| `10`<sub>h</sub> | `void*` | semantic | descriptor at `01F2CE40`..., null for none |

Channel semantic, `18`<sub>h</sub> bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `void*` | name |  |
| `08`<sub>h</sub> | `void*` | link | 0 in the image |
| `10`<sub>h</sub> | `u32` | floats |  |
| `14`<sub>h</sub> | `u32` | index | 0 in the image |

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

`PAnimationNetworkNode` (`138`<sub>h</sub> bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `100`<sub>h</sub> | `u32` | inputCount | bit 31 masked |
| `108`<sub>h</sub> | `void*` | inputs | `10`<sub>h</sub> bytes each: source node at +`00`<sub>h</sub>, output index at +`08`<sub>h</sub> |
| `110`<sub>h</sub> | `u32` | outputCount | bit 31 masked |
| `118`<sub>h</sub> | `void*` | outputs | `0C`<sub>h</sub> bytes each: size, state (0, 1 placed, 2 released), slot |
| `120`<sub>h</sub> | `u32` | readerCount | bit 31 masked |
| `128`<sub>h</sub> | `void*` | readers | nodes that read this node's outputs |
| `130`<sub>h</sub> | `i32` | order | -1 until scheduled |

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
  size is `40`<sub>h</sub>.
- A misspelt data-member path binds nothing and logs nothing; an out-of-range array index is logged.
- Setting a target record's kind to 0 disables that channel's group.

## Related

- [Phyre reflection](phyre-reflection.md): class descriptors, member records and array kinds the binder walks.
- [Phyre field schema](phyre-field-schema.md): file-side against runtime member layouts.
- [Phyre asset files](phyre-asset-files.md): the clusters that carry animation sets.
- [Vtable methods](../Engine-Core/vtable-methods.md): the vtable slot convention used here.
