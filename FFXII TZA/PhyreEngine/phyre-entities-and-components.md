---
title: "Phyre entities and components: PEntity, its component list, the world-matrix registry and the hooks that run on loaded components"
kind: "system"
category: "PhyreEngine"
addresses: "0x006AB7E0, 0x006AC300, 0x006ACA70, 0x006ACAC0, 0x006ABEC0, 0x006ABF40, 0x006AB600, 0x006ABFA0, 0x006AB410, 0x006AADD0, 0x006AFF00, 0x006AF4F0, 0x0069ECE0, 0x01F2EB40, 0x01F2EB78, 0x02E4EAF0, 0x02E4E720, 0x0067F6F0"
---

## What the player sees

Nothing directly. An entity is PhyreEngine's container for an object placed in a scene: it owns a
world matrix and a list of components. The engine uses the registry on this page to answer "which
entity does this matrix, or this object, belong to", for example when a physics body reports a
contact.

## How it works

### Entities and components

A `PEntity` (descriptor `0x02E4EAF0`, `0x38` bytes) holds the first of its components at `+0x00`, its
world matrix at `+0x08` and a node of the world-matrix registry at `+0x10`. A `PComponent`
(descriptor `0x02E4E720`, `0x18` bytes) holds the next component at `+0x00`, its entity at `+0x08` and
its own class descriptor at `+0x10`. Six classes derive from `PComponent`: `PAnimatableComponent`,
`PInstancesComponent`, `PNameComponent`, `PQuarryComponent`, `PScriptableComponent` and
`PTriggerReceiverComponent`.

The registrar `0x006AB7E0` publishes the entity's script methods, each as a method record whose
function sits `0x30` bytes in, and the member `m_firstComponent`:

| Method | Function | What it does |
|---|---|---|
| `getComponent` | `0x006ACA10` | walks the list and returns the first component whose class is the given class or derives from it |
| `getWorldMatrix` | `0x006B5C70` | returns `+0x08` |
| `setWorldMatrix` | `0x006ACAC0` | moves the entity in the registry to the new matrix |
| `addComponent` | `0x006AC300` | adds a component at the front of the list |
| `removeComponent` | `0x006ACA70` | unlinks a component |
| `FindEntityForWorldMatrix` | `0x006ABF40` | looks a matrix up in the registry |
| `FindEntityForObj` | `0x006ABEC0` | finds the matrix of any object, then its entity |

### Adding and removing components

`0x006AC300(entity, component)` returns 0 at once when the component already belongs to this entity.
It returns `0x12` when the component's class does not derive from `PComponent`, and also when the
entity already has a component whose class is the same as, an ancestor of or a descendant of the new
one's, so an entity holds at most one component of each line of classes. Otherwise it removes the
component from its old entity (`0x006ACA70`), sets its entity and links it at the front.

`0x006ACA70(entity, component)` returns 5 when the component belongs to another entity; otherwise it
unlinks it from the list and clears its entity.

### The world-matrix registry

The entities are kept in an ordered tree headed by the six qwords at `0x01F2EB40` (root at
`0x01F2EB58`), keyed by world-matrix address. It is the same tree code as the asset-name registry of
the memory page: `0x0067F700` rebalances after an insert, `0x0067FE20` erases a node and `0x0067F6F0`
points a head's three links back at itself.

- `0x006ACAC0(entity, matrix)` erases the entity's node when it had a matrix, stores the new one and,
  unless that matrix is already registered, inserts the node with the matrix as key and the entity
  as value.
- `0x006ABF40(matrix)` walks the tree from the root and returns the entity, or null.
- `0x006ABEC0({object, class})` uses the object itself when its class is `PWorldMatrix` (`0x02E404B0`)
  or derives from it. Otherwise it looks up the class's `getLocalToWorldMatrix` method
  (`0x005A7B50`) and calls it through `0x006AB600`, which calls slot `+0x10` of the handler at the method's
  `+0x28` with the object and takes the matrix from the result. It then looks the matrix up like `0x006ABF40`.

### Loaded entities and components

Descriptor slot `+0x70` runs on each instance list a cluster load fixes up (the asset-file page). For
these classes it walks the list's objects, using the class's instance size (`+0x38` of the
descriptor) as the stride:

- `PEntity`: `0x006AB410` passes the list to `0x006ABFA0`, which inserts every entity with a world matrix
  into the registry, skipping a matrix already present.
- Components: `0x006AADD0` sets each component's class pointer `+0x10` to the list's descriptor. It is
  slot `+0x70` itself for `PTriggerReceiverComponent` (through `0x006ADD70`) and is called first by
  the `PAnimatableComponent` hook `0x005B80E0` (through `0x005A2610`) and by `0x006AFF00`.
- `PNameComponent`: `0x006AFF00` (through `0x006AFA70`) also links every name component at the front of
  the list headed at `0x01F2EB78`, through a `{next, previous}` node at `+0x18`.

### Instances components

`0x006AF4F0(component, &result, class)`, a method that `0x006AE350` registers for
`PInstancesComponent`, searches the component's array of 16-byte `{object, class}` pairs
(`+0x18` count, `+0x20` data) for the first pair whose class is the given class or derives from it,
and returns that pair. With none, or with a null class, it returns a null object with the `PBase`
descriptor (`0x02CF8270`, from `0x006372A0`).

### The object behind a physics body

`0x0069ECE0(collision object, record)` fills `+0x20` and `+0x28` of a physics callback record with the
gameplay object behind a Bullet collision object and its class: when bit `0x2` of the object's type
word `+0x104` is set, the pointer at `+0x108` with `PPhysicsRigidBody`'s descriptor (`0x02E48BD0`);
when the type is 4, the same pointer with `PPhysicsCharacterController`'s (`0x02E47ED0`). A null
pointer leaves both null. The physics functions `0x006A1A70` and `0x006A1DD0` call it.

## Layouts

### Reflected members

The members below are the ones the code of this page's classes uses or the reflection registers; each registered member is named by its registration (the registering function, through 0x00632960), and each class fence covers only those members.

`PNameComponent` (`0x30` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x28` | `void*` | m_name | m_name (ptr), registered by `0x006AFC20` (`0x00632960` at `0x006AFCB2`); no shipped .phyre file declares PNameComponent |

`PQuarryComponent` (`0x68` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x48` | `f32[4]` | m_min | m_min (f32[4]), registered by `0x006A9840` (`0x00632960` at `0x006A993C`); no shipped .phyre file declares PQuarryComponent |
| `+0x58` | `f32[4]` | m_size | m_size (f32[4]), registered by `0x006A9840` (`0x00632960` at `0x006A99AB`); no shipped .phyre file declares PQuarryComponent |

`PScriptableComponent` (`0x40` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x20` | `void*` | m_entryPoint | m_entryPoint (ptr), registered by `0x006CD000` (`0x00632960` at `0x006CD0FF`); no shipped .phyre file declares PScriptableComponent |
| `+0x30` | `u8[16]` | bytes30 | `+0x30` to `+0x3F`; no registered member covers it (`0x006CCF50` registers the `0x40`-byte class at `0x006CCF9A`) |

`PTriggerReceiverComponent` (`0x58` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x24` | `u8[4]` | bytes24 | the four bytes after the dword the constructor `0x006CDF00` clears at `+0x20` (`0x006CDF36`), before m_entryHandler at `+0x28`; no registered member covers it (`0x006CDFF0` registers the `0x58`-byte class at `0x006CE03A`) |

### Entities and components

The structures below are the ones the mechanisms above use.

`PEntity` (`0x38` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | m_firstComponent | first PComponent, or null |
| `+0x08` | `void*` | worldMatrix | PWorldMatrix; the registry key |
| `+0x10` | `void*` | left | registry node |
| `+0x18` | `void*` | right |  |
| `+0x20` | `u64` | parent | parent node; bit `0x1` is the node colour |
| `+0x28` | `void*` | key | the world matrix again |
| `+0x30` | `void*` | value | this entity |

`PComponent` (`0x18` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | next | next component of the entity |
| `+0x08` | `void*` | entity | owning PEntity, or null |
| `+0x10` | `void*` | classDescriptor | set by `0x006AADD0` on load and checked by `0x006AC300` |

## State

| Address | What |
|---|---|
| `0x01F2EB40` | head of the world-matrix registry; root at `0x01F2EB58` |
| `0x01F2EB78` | head of the list of loaded `PNameComponent` objects |
| `0x02E4EAF0` | `PEntity` class descriptor |
| `0x02E4E720` | `PComponent` class descriptor |

## Modding notes

- An entity accepts one component of each line of classes; adding a second component of a related
  class fails with `0x12` and changes nothing.
- The registry is keyed by the world matrix's address, so two entities sharing one matrix cannot both
  be found; only the first registered is kept.
- Changing an entity's matrix pointer directly leaves the registry pointing at the old matrix; use
  `setWorldMatrix`.

## Related

- [Phyre reflection](phyre-reflection.md): class descriptors, their slots and the instance lists these hooks walk.
- [Phyre asset files](phyre-asset-files.md): the cluster load that calls slot `+0x70`.
- [Memory and allocation](../Compiler-And-C-Runtime/memory-and-allocation.md): the asset-name registry built on the same tree.
- [Phyre Lua bindings](phyre-lua-bindings.md): the script method records these registrations fill.
